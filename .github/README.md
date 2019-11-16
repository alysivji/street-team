# GitHub

This folder contains settings related to GitHub features.

## GitHub Workflow Notes

**workflow** -- must have at least one job
**jobs** -- contains a series of steps that perform individual tasks
**steps** -- run commands or use an action (create your own, use community created)

> You can configure a workflow to start when a GitHub event occurs, on a schedule, or from an external event.
> When choosing the type of actions to use in your workflow, we recommend exploring existing actions in public repositories or on Docker hub and potentially customizing these actions for your project.

## Todo

- [ ] environment
- [ ] use checkout action to copy repo's code into CI
  - uses: actions/checkout@v1
- [ ] [workflow status badge](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/configuring-a-workflow#adding-a-workflow-status-badge-to-your-repository)
 - `https://github.com/<OWNER>/<REPOSITORY>/workflows/<WORKFLOW_NAME>/badge.svg`
 - `https://github.com/<OWNER>/<REPOSITORY>/workflows/<WORKFLOW_FILE_PATH>/badge.svg`
- actions/upload-artifact and actions/download-artifact

 ## Useful Resources

 - [Core concepts for GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/core-concepts-for-github-actions)
- [Persisting data u sing artifacts](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/persisting-workflow-data-using-artifacts)
- [Workflow Syntax for GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions)
