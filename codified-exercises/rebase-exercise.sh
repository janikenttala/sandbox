#!/bin/sh

myerr(){
  echo "ERR:" $* 1>&2
  exit 1
}

cd $(dirname $0) || myerr "Failed to move to working directory"
mydir=$(pwd)

[ $(basename $(pwd)) != "codified-exercises" ]|| myerr "Move this script away from repo"

EXERCISE="${mydir}/rebase-exercise"
origin="${EXERCISE}/origin"
mylocalrepo="${EXERCISE}/rebaserepo-my"
somebodyelse="${EXERCISE}/rebaserepo-somebodyelse"

mkdir ${EXERCISE}
cd ${EXERCISE} || myerr "Failed to move to exercise dir"

# First we'll create the repo which simulates the "origin".
# This could be your github site in real-world

git init ${origin} || myerr "Repo init failed"

cd ${origin}

echo "First commit to master..."
echo "master of puppets" > worked-in-master.txt
git add worked-in-master.txt
git commit -m "1st commit to master"
git checkout -b "null" #to allow pushes, origin/master can not be checked out

# Now, we will clone the origin for ourselves.
# After clone, we already start working in our own branch.
git clone ${origin} ${mylocalrepo}
cd ${mylocalrepo}

echo "Branch and commit"
git checkout -b lagger
echo "slave new world" > worked-in-local.txt
git add worked-in-local.txt
git commit -m "1st commit to local 'topic' branch"

# While we are working, somebody else commits to origin/master
# a bunch of commits (we will use another clone to simulate this)

cd ${EXERCISE}
git clone ${origin} ${somebodyelse}

cd ${somebodyelse} || myerr "failed to move to repo"
git checkout master

echo "2nd commit to master..."
echo "is pulling your strings" > worked-in-master.txt
git add worked-in-master.txt
git commit -m "2nd commit to master"

echo "3rd commit to master..."
echo "blinded by me you can't see a thing" > worked-in-master.txt
git add worked-in-master.txt
git commit -m "3rd commit to master"

git push --set-upstream origin master

# You continue to work with your own branch
cd ${mylocalrepo} || myerr "Moving to ${mylocalrepo} failed"
git checkout lagger
echo "Face the enemy" > worked-in-local.txt
git add worked-in-local.txt
git commit -m "2nd commit to local 'topic' branch"

# Now you realise, that you are behind the origin/master quite a lot.
# You think you should not duplicate a bunch of commits made by others,
# when you commit/push to origin.  Instead of merge, you decide to rebase.

git fetch origin || myerr "Git fetch origin failed"
git rebase origin/master || myerr "Rebase failed"

# Merge your branch to master (In github, this could happen via pull request)
git checkout master
git merge lagger master
git push

# You are done, time to get rid of your branch
git branch -d lagger
