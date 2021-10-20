# How to contribute

LRG-omics is open source and welcomes your contributions! This document
describes how to merge code changes into RG-omics.

Please report bugs or requests to improve LRG-omics through the Issue Tracker.
Contributions are welcome, and they are highly appreciated!

These are some points to keep in mind:

- To report bugs please inlcude:

    - Your operating system (name and version).
    - Details about your local setup (environments, versions of dependencies, etc).
    - Step-by-step description to reproduce the bug.

- Documentation:

We are currently building our docs, then any help to make our docs better is also very appreciated!


## Getting Started

* Make sure you have a [GitHub account](https://github.com/signup/free).
* [Fork](https://help.github.com/articles/fork-a-repo/) this repository on GitHub.
* On your local machine,
  [clone](https://help.github.com/articles/cloning-a-repository/) your fork of
  the repository.

## Development branch


Please note that current development on LRG-omics is limited to Linux OS. We are
planning to implement MacOS and Windows in the near future. To set up LRG-omics
for local development please follow the steps outlined below:

1. Fork lrg-omics using the “Fork” button.

1. Create and activate the development environment:

    ```
    conda create -f dev/conda/environment.yml
    conda activate lrg-omics-dev
    ```

1. Clone your forked repo locally in your preferred location:

    ```
    git clone git@github.com:YOURGITHUBNAME/lrg-omics.git
    ```

1. Create a branch for local development:

    ```
    git checkout -b your-branch-name
    git switch your-branch-name
    ```

    Now you're ready to make changes locally!

## Making Changes

* Add some really awesome code to your local fork.  It's usually a [good
  idea](http://blog.jasonmeridth.com/posts/do-not-issue-pull-requests-from-your-master-branch/)
  to make changes on a
  [branch](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/)
  with the branch name relating to the feature you are going to add.
* When you are ready for others to examine and comment on your new feature,
  navigate to your fork of membrane_curvature on GitHub and open a [pull
  request](https://help.github.com/articles/using-pull-requests/) (PR). Note that
  after you launch a PR from one of your fork's branches, all
  subsequent commits to that branch will be added to the open pull request
  automatically.  Each commit added to the PR will be validated for
  mergability, compilation and test suite compliance; the results of these tests
  will be visible on the PR page.
* If you're providing a new feature, you must add test cases and documentation.
* When the code is ready to go, make sure you run the test suite using pytest.
* When you're ready to be considered for merging, check the "Ready to go"
  box on the PR page to let the membrane_curvature devs know that the changes are complete.
  The code will not be merged until this box is checked, the continuous
  integration returns checkmarks,
  and multiple core developers give "Approved" reviews.

## Test coverage

LRG-omics uses [pytest] framework. You can run the tests in three steps:


1. Install 

    ```bash
    pip install pytest-cov
    ```

1. Go to the root folder of LRG-omics:

    ```
    cd lrg-omics    
    ```

1. Then you can run pytest with a coverage report in HTML with:

    ```
    pytest --cov=lrg-omics --cov-report=html
    ```


When submitting a Pull Request, all tests should pass.

# Additional Resources

* [General GitHub documentation](https://help.github.com/)
* [PR best practices](http://codeinthehole.com/writing/pull-requests-and-other-good-practices-for-teams-using-github/)
* [A guide to contributing to software packages](http://www.contribution-guide.org)
* [Thinkful PR example](http://www.thinkful.com/learn/github-pull-request-tutorial/#Time-to-Submit-Your-First-PR)