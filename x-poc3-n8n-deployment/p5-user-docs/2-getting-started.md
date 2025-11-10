# Getting Started with N8N

**For**: Business Users
**Purpose**: Learn the basics of the N8N interface
**Date**: November 8, 2025

---

## Welcome to N8N!

Now that you're logged in, let's get familiar with what you see on your screen.

---

## The N8N Dashboard

When you first log in, you'll see the **Dashboard** - this is your home base.

### What You'll See:

**1. Left Sidebar** (Navigation Menu)
- **Workflows**: All your automations
- **Templates**: Ready-made workflows you can use
- **Credentials**: Where you store login info for other apps
- **Executions**: History of workflows that have run
- **Settings**: Your account settings

**2. Main Area** (Center)
- This is where you'll build workflows
- When starting out, you'll see a welcome screen or empty workspace

**3. Top Bar**
- Your account info (top right)
- Help and documentation
- Notifications

---

## Key Concepts (Simple Terms)

### What is a Workflow?

A **workflow** is a set of steps that happen automatically. Think of it like a recipe:
- Step 1: When this happens...
- Step 2: Do this...
- Step 3: Then do that...

**Example**: "When I receive an email with an invoice, save it to my cloud storage and notify me"

### What is a Node?

A **node** is one step in your workflow. Each node does one thing:
- Read an email
- Send a message
- Save a file
- Calculate a number

You connect nodes together to create a complete workflow.

### What is a Trigger?

A **trigger** is what starts your workflow. Common triggers:
- A new email arrives
- A file is uploaded
- A specific time (like every Monday at 9am)
- A webhook receives data

---

## Your First Tour

Let's explore the interface together!

### Step 1: Workflows Page

**Click "Workflows" in the left sidebar**

You'll see:
- **"New Workflow"** button (top right) - Click this to create a new automation
- List of existing workflows (empty at first)
- Search and filter options

### Step 2: Templates

**Click "Templates" in the left sidebar**

This is a library of ready-made workflows! You'll find:
- Popular automation examples
- Workflows organized by category (Email, CRM, Data Processing, etc.)
- **Tip**: Start here! Pick a template and modify it for your needs

### Step 3: Credentials

**Click "Credentials" in the left sidebar**

This is where you store login information for apps you want to connect:
- Email accounts
- Cloud storage (Google Drive, Dropbox, etc.)
- Business tools (Slack, Salesforce, etc.)

**Security Note**: Your credentials are encrypted and secure!

---

## Understanding the Workflow Editor

### Step 1: Create a New Workflow

**Click "Workflows" → "New Workflow"**

You'll see:
- A large canvas (blank workspace)
- A panel on the right with available nodes
- A plus (+) button in the center

### Step 2: The Canvas

This is your workspace where you build:
- **Drag and drop** nodes onto the canvas
- **Connect** nodes by dragging lines between them
- **Zoom** in/out using your mouse wheel or touchpad

### Step 3: Adding Nodes

**Click the "+" button on the canvas**

You'll see a menu with node categories:
- **Trigger**: What starts your workflow
- **Action**: What your workflow does
- **Logic**: Make decisions (if/then)
- **Transform**: Change or format data

---

## Common Workflow Patterns

Here are typical workflows business users create:

### Pattern 1: Email to File Storage
```
New Email → Extract Attachment → Save to Google Drive → Send Notification
```

### Pattern 2: Scheduled Report
```
Every Monday 9am → Get Data from Database → Format Report → Email Report
```

### Pattern 3: Approval Process
```
Form Submitted → Send to Manager → Wait for Approval → Update System
```

### Pattern 4: Data Sync
```
New Row in Spreadsheet → Validate Data → Create Record in CRM
```

---

## Tips for Getting Started

### Tip 1: Start with Templates
- Don't build from scratch at first!
- Find a template close to what you need
- Modify it to fit your exact requirements

### Tip 2: Test as You Build
- After adding each node, click the "Execute" button
- Check if that step works before adding the next one
- This makes troubleshooting easier

### Tip 3: Use the Help Panel
- Click on any node to see help documentation
- N8N provides examples for each node type
- Look for the "?" icon or "Help" link

### Tip 4: Save Frequently
- Click "Save" in the top right corner often
- Give your workflow a descriptive name
- N8N also auto-saves, but better safe than sorry!

### Tip 5: Keep It Simple
- Start with simple workflows (2-3 steps)
- Once you're comfortable, add more complexity
- A working simple workflow is better than a complex broken one

---

## Quick Actions Reference

| What You Want to Do | How to Do It |
|---------------------|--------------|
| Create new workflow | Workflows → New Workflow |
| Use a template | Templates → Pick one → Use This Workflow |
| Add a node | Click + on canvas |
| Connect nodes | Drag from one node's output to another's input |
| Test a workflow | Click "Execute Workflow" button (top) |
| Save your work | Click "Save" button (top right) |
| Get help | Click ? icon or Help in top menu |

---

## Common Questions

**Q: Can I break anything?**
**A**: No! You're in a safe environment. Experiment freely. The worst that can happen is a workflow doesn't work, and you can always start over.

**Q: What if I make a mistake?**
**A**: Use "Undo" (Ctrl+Z or Cmd+Z) to reverse your last action. You can also just delete a node and try again.

**Q: How many workflows can I create?**
**A**: As many as you need! There's no limit in your N8N instance.

**Q: Can I share workflows with coworkers?**
**A**: Yes! You can export workflows and share them. (We'll cover this in advanced guides)

**Q: What if a workflow stops working?**
**A**: Check the "Executions" page to see what went wrong. N8N shows error messages that help you fix the issue.

---

## Your Next Steps

Now you're ready to:
1. **Browse Templates** - Find automation ideas
2. **Create Your First Workflow** - See "3-first-workflow.md"
3. **Connect Your Apps** - Add credentials for tools you use

---

## Need Help?

**In N8N**:
- Click the **?** icon (Help menu)
- Visit **Templates** for examples
- Check **Documentation** in the help menu

**Technical Support**:
- Contact your IT Administrator
- Check the Governance folder for technical docs
- Email: support@hx.dev.local

---

**Remember**: Learning automation takes practice. Start small, experiment, and build confidence!

---

**Document Version**: 1.0
**Last Updated**: November 8, 2025
**Classification**: Internal Use Only
