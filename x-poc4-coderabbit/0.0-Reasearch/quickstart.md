# Quickstart

> This tutorial gives you a hands-on demonstration of CodeRabbit, using a real GitHub repository. It guides you through the following tasks:

<Steps>
  <Step title="Integrate CodeRabbit into a GitHub repository that you own" />

  <Step title="Observe CodeRabbit perform a code review of a pull request that you initiate" />

  <Step title="Converse with CodeRabbit about the code review" />

  <Step title="Prompt CodeRabbit to generate its own improvements to the pull request" />
</Steps>

When you complete this tutorial, you'll have seen CodeRabbit's code-review
feature in action, and glimpsed a few of its other AI-driven abilities as well.

For a more general overview of CodeRabbit, see [Introduction](/).

<Note>
  While this tutorial focuses on GitHub, CodeRabbit also works with GitLab,
  Azure DevOps, and Bitbucket. For more information, see [Integrate with Git
  platforms](/platforms/).
</Note>

## Before you begin[​](#before-you-begin "Direct link to Before you begin")

Create a new, private repository on GitHub. Name the new repository `coderabbit-test`, and let it have otherwise default GitHub settings.

## Integrate CodeRabbit with your GitHub account[​](#integrate-coderabbit-with-your-github-account "Direct link to Integrate CodeRabbit with your GitHub account")

To integrate CodeRabbit with your GitHub account, follow these steps:

<Steps>
  <Step title="Create an account">
    Visit [the CodeRabbit login
    page](https://app.coderabbit.ai/login?free-trial).
  </Step>

  <Step title="Login with your git provider">Click **Login with GitHub**.</Step>
  <Step title="Authorize">Click **Authorize coderabbitai**.</Step>
</Steps>

CodeRabbit takes a moment to set up the integration. After it finishes, the CodeRabbit dashboard appears.

## Add CodeRabbit to your repository[​](#add-coderabbit-to-your-repository "Direct link to Add CodeRabbit to your repository")

To add CodeRabbit to your test repository, follow these steps:

<Steps>
  <Step title="Access repository settings">
    On the CodeRabbit dashboard, click **Add Repositories**. A GitHub
    repository-access dialog appears.
  </Step>

  <Step title="Grant repository access">
    Select the **Only select repositories** radio button.
  </Step>

  <Step title="Select your test repository">
    From the **Select repositories** menu, select the `coderabbit-test`
    repository that you created earlier in this Quickstart.
  </Step>

  <Step title="Install and authorize CodeRabbit">
    Click **Install & Authorize**.

    <Note>
      CodeRabbit requests read and write access to your repository in order for
      its code review, issue management, and pull request generation features to
      work. CodeRabbit never stores your code. For more information, see [the
      CodeRabbit Trust Center](https://trust.coderabbit.ai).
    </Note>
  </Step>

  <Step title="Complete signup if prompted">
    If a CodeRabbit **Complete your signup** dialog appears, then fill it out
    with the requested information before continuing.
  </Step>
</Steps>

CodeRabbit is now ready to use with your test repository. The next steps demonstrate its core code-review features.

## Let CodeRabbit perform a code review[​](#let-coderabbit-perform-a-code-review "Direct link to Let CodeRabbit perform a code review")

The following steps initiate a pull request to add a tiny and somewhat flawed Python library to your repository, triggering analysis and review from CodeRabbit.

Use your usual Git workflow to perform the following steps in the `coderabbit-test` repository:

<Steps>
  <Step title="Create a branch">
    Create a branch named `add-utils`.
  </Step>

  <Step title="Create a new file">
    In that new `add-utils` branch, create a new file called `simple_utils.py`, with the following content:

    ```python  theme={null}
    # simple_utils.py - A tiny utility library

    def reverse_string(text):
        """Reverses the characters in a string."""
        return text[::-1]

    def count_words(sentence):
        return len(sentence.split())

    def celsius_to_fahrenheit(celsius):
        return (celsius * 9/5) + 32
    ```
  </Step>

  <Step title="Commit the file">
    Commit the added file to the `add-utils` branch. Use any text you want for the commit message.
  </Step>

  <Step title="Create a pull request">
    Create a pull request that proposes to merge the `add-utils` branch into the `main` branch. Use any text you want for the pull request message.
  </Step>
</Steps>

After a few moments, CodeRabbit responds to the pull request using the `@coderabbitai` GitHub account. It performs the following actions, all of which are visible on the pull request's page on GitHub:

* If you didn't write a pull request summary, then CodeRabbit adds a new summary to the pull request.
* CodeRabbit posts a comment titled **Walkthrough** containing analysis and commentary about the content of the pull request.
* CodeRabbit attaches a detailed code review to the pull request as another comment.

Part of the review resembles the following screenshot:

<img src="https://mintcdn.com/coderabbit/D_rqUjBaYiE185JH/images/getting-started/assets/images/quickstart-comment-9310a2af173d5afbd2c74a762e6bd808.png?fit=max&auto=format&n=D_rqUjBaYiE185JH&q=85&s=159b85cdd77b56e33b809b0d3d4cb7cb" alt="An example code review comment" data-og-width="1624" width="1624" data-og-height="964" height="964" data-path="images/getting-started/assets/images/quickstart-comment-9310a2af173d5afbd2c74a762e6bd808.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/coderabbit/D_rqUjBaYiE185JH/images/getting-started/assets/images/quickstart-comment-9310a2af173d5afbd2c74a762e6bd808.png?w=280&fit=max&auto=format&n=D_rqUjBaYiE185JH&q=85&s=49572f912d1556c1e2100c8b261a672a 280w, https://mintcdn.com/coderabbit/D_rqUjBaYiE185JH/images/getting-started/assets/images/quickstart-comment-9310a2af173d5afbd2c74a762e6bd808.png?w=560&fit=max&auto=format&n=D_rqUjBaYiE185JH&q=85&s=db43f41c858bb4c35be61c3e9817bcfe 560w, https://mintcdn.com/coderabbit/D_rqUjBaYiE185JH/images/getting-started/assets/images/quickstart-comment-9310a2af173d5afbd2c74a762e6bd808.png?w=840&fit=max&auto=format&n=D_rqUjBaYiE185JH&q=85&s=fcf1ba9035aefc14e7fbe2dc53f2d7b5 840w, https://mintcdn.com/coderabbit/D_rqUjBaYiE185JH/images/getting-started/assets/images/quickstart-comment-9310a2af173d5afbd2c74a762e6bd808.png?w=1100&fit=max&auto=format&n=D_rqUjBaYiE185JH&q=85&s=2719c7e5252c0e2deb556ff648ec7b61 1100w, https://mintcdn.com/coderabbit/D_rqUjBaYiE185JH/images/getting-started/assets/images/quickstart-comment-9310a2af173d5afbd2c74a762e6bd808.png?w=1650&fit=max&auto=format&n=D_rqUjBaYiE185JH&q=85&s=0e5be4b0cc953c8b3f2c88a265be438e 1650w, https://mintcdn.com/coderabbit/D_rqUjBaYiE185JH/images/getting-started/assets/images/quickstart-comment-9310a2af173d5afbd2c74a762e6bd808.png?w=2500&fit=max&auto=format&n=D_rqUjBaYiE185JH&q=85&s=dfd73185019b0c8130d3a2fe87b50d47 2500w" />

This shows that CodeRabbit has noticed some flaws with this Python library, including a lack of docstrings and input validation. The review comment identifies these flaws, and suggests how you might improve them.

## Ask CodeRabbit for more information[​](#ask-coderabbit-for-more-information "Direct link to Ask CodeRabbit for more information")

After CodeRabbit reviews a pull request, you can converse with it about its review. You can also give CodeRabbit special commands to request it to perform specific functions, such as generating appropriate code changes for you.

1. Post the following as a new GitHub comment attached to the pull request:

   ```text Chat in PR wrap theme={null}
   @coderabbitai Why do all of these functions need docstrings? Isn't it obvious enough what they do?
   ```

   After a few moments, CodeRabbit posts its reply, explaining its motivations for its recommendation. The reply might resemble the following:

   > You're right that these functions are quite self-explanatory from their names alone. Docstrings aren't strictly necessary for every function, especially in smaller projects with clear function names.
   >
   > While docstrings do provide benefits (IDE tooltips, documentation generation, help for future developers), they can sometimes feel redundant for very straightforward functions. It's ultimately a matter of coding style and project requirements.
   >
   > If you prefer to skip docstrings for obvious utility functions in this project, that's perfectly reasonable. Would you like me to adjust my review approach regarding documentation for this repository?

   In this case, CodeRabbit is offering to adjust its future behavior when reviewing changes to this repository. Instead, follow the next step to ask CodeRabbit to implement part of its suggestions.

2. Post the following as another new comment:

   ```text  theme={null}
   @coderabbitai generate docstrings
   ```

   After a few moments, CodeRabbit does the following:

   * CodeRabbit creates a new branch, based on `add-utils`.
   * CodeRabbit commits changes to the branch that adds suggested docstrings to `add-utils`.
   * CodeRabbit opens a new pull request between the new branch and `add-utils`.

## Clean up[​](#clean-up "Direct link to Clean up")

Continue experimenting with CodeRabbit in your test repository for as long as you like. When you're finished, you can delete the repository.

You are now ready to add CodeRabbit to other repositories that you own, and let it review some real pull requests.

## What's next[​](#whats-next "Direct link to What's next")

* [Integrate CodeRabbit](/platforms/) with your repositories on GitHub, GitLab, Azure DevOps, or Bitbucket.
* [Configure CodeRabbit](/getting-started/configure-coderabbit) beyond its default settings.
* [Add custom review instructions](/guides/review-instructions).
* [Get support for CodeRabbit](/getting-started/support).
* [Learn more about how CodeRabbit works](/overview/why-coderabbit).

[Edit this page](https://github.com/coderabbitai/coderabbit-docs/edit/main/docs/getting-started/quickstart.md)

Last updated on **Jul 31, 2025**
