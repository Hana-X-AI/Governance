# Creating Your First N8N Workflow

**For**: Business Users
**Purpose**: Step-by-step tutorial to create a simple automation
**Date**: November 8, 2025

---

## What We'll Build

In this guide, you'll create a simple workflow that:
1. Runs on a schedule (every day at 9am)
2. Gets data from a source
3. Sends you a notification

This is a great starter workflow because:
- It's simple (only 3 steps)
- It teaches you the basics
- You can see it work immediately
- You can build on it later

---

## Tutorial: Daily Morning Notification

### Step 1: Create a New Workflow

**Action**:
1. Click **"Workflows"** in the left sidebar
2. Click **"New Workflow"** button (top right)

**What You'll See**:
- A blank canvas with a "+" button in the center
- The words "My Workflow" at the top (we'll rename this)

**First, Let's Rename It**:
1. Click on "My Workflow" at the top
2. Type a new name: `My First Workflow - Daily Test`
3. Press Enter

---

### Step 2: Add a Schedule Trigger

Every workflow needs a **trigger** - something that starts it.

**Action**:
1. Click the **"+"** button on the canvas
2. In the search box, type: `schedule`
3. Click **"Schedule Trigger"**

**Configure the Schedule**:
1. You'll see the Schedule Trigger node appear
2. Click on the node to open its settings
3. Look for "Trigger Interval"
4. Set it to: **"Every Day"**
5. Set time to: **"9:00 AM"**
6. Close the settings (or click away)

**What This Does**:
- Your workflow will run automatically every morning at 9am
- No manual action needed!

---

### Step 3: Add a Simple Action Node

Now let's add something that actually does something.

**Action**:
1. Hover over your Schedule Trigger node
2. Click the **"+"** button that appears to the right
3. In the search box, type: `set`
4. Click **"Set"** (under "Data transformation")

**Configure the Set Node**:
1. Click on the Set node to open settings
2. Click **"Add Value"**
3. Select **"String"** (text)
4. In "Name" field, type: `message`
5. In "Value" field, type: `Good morning! Your workflow is working!`
6. Close the settings

**What This Does**:
- Creates a simple message
- We'll use this message in the next step

---

### Step 4: Test Your Workflow (So Far)

Before adding more, let's make sure it works!

**Action**:
1. Look at the top of the screen
2. Click the **"Execute Workflow"** button

**What Happens**:
- Your workflow runs immediately (testing mode)
- Green checkmarks appear on nodes that work
- Red X's appear if something went wrong

**Check Your Results**:
1. Click on the Set node
2. Look for "Output Data" section
3. You should see your message: "Good morning! Your workflow is working!"

**Success!** Your workflow is working so far.

---

### Step 5: Add a Notification (Email or Webhook)

For this tutorial, we'll keep it simple and just show the output. In a real workflow, you'd send an email or notification.

**For Now, Let's Just Document the Output**:
1. Your workflow is complete!
2. The Set node shows you the data it created
3. In a real scenario, you'd add:
   - An "Email" node to send yourself the message
   - A "Slack" node to post to a channel
   - An "HTTP Request" node to call another system

---

### Step 6: Save Your Workflow

**Very Important - Save Your Work!**

**Action**:
1. Look at top right corner
2. Click **"Save"** button
3. You'll see "Workflow saved" confirmation

**Your workflow is now permanent!**

---

### Step 7: Activate Your Workflow

Right now, your workflow exists but won't run automatically.

**Action**:
1. Look for the toggle switch at the top (near "Save" button)
2. It says "Inactive" - click it to turn it **ON**
3. It should now say **"Active"**

**What This Means**:
- Your workflow will now run automatically at 9am every day
- You don't need to do anything - it runs on its own!

---

## Understanding What You Built

Let's review what each part does:

### Schedule Trigger (First Node)
- **Purpose**: Starts your workflow automatically
- **When**: Every day at 9:00 AM
- **Action**: Triggers the next node in the chain

### Set Node (Second Node)
- **Purpose**: Creates data (your message)
- **When**: Immediately after the trigger fires
- **Action**: Passes the message to the next node

---

## What Happens When Your Workflow Runs

**Tomorrow Morning at 9am**:
1. N8N wakes up and checks: "Any workflows scheduled for 9am?"
2. Finds your workflow: "My First Workflow - Daily Test"
3. Runs the Schedule Trigger
4. Runs the Set node
5. Creates your message
6. Workflow completes!

---

## Viewing Workflow History

Want to see if your workflow ran?

**Action**:
1. Click **"Executions"** in the left sidebar
2. You'll see a list of every time your workflow ran
3. Click on any execution to see details

**What You'll See**:
- Date and time it ran
- Whether it succeeded (green) or failed (red)
- How long it took
- What data was processed

---

## Next Steps: Make It More Useful

Now that you have a working workflow, let's make it actually do something!

### Add an Email Node

**To Send Yourself an Email**:
1. Edit your workflow
2. Click the "+" after the Set node
3. Search for "Email" and select "Send Email"
4. Configure:
   - **To**: `caio@hx.dev.local`
   - **Subject**: `Your Daily N8N Workflow Report`
   - **Text**: Use the message from the Set node

### Add Conditional Logic

**To Make Decisions**:
1. Add an "IF" node after Set
2. Check if today is Monday
3. If yes: Send one message
4. If no: Send a different message

### Connect to Real Apps

**Popular Integrations**:
- **Gmail**: Send/receive emails
- **Slack**: Post messages
- **Google Sheets**: Read/write spreadsheet data
- **Salesforce**: Update CRM records
- **Dropbox**: Manage files

To use these, you'll need to:
1. Go to "Credentials" page
2. Add your login info for that app
3. N8N will connect securely

---

## Common Challenges (And How to Fix Them)

### Problem: "Workflow didn't run at 9am"

**Troubleshooting**:
1. Check if workflow is **Active** (toggle switch ON)
2. Check "Executions" page for errors
3. Verify the schedule is set correctly (9:00 AM, not 9:00 PM!)
4. Make sure N8N server is running (contact IT if unsure)

### Problem: "Can't connect nodes"

**Solution**:
- Drag from the **small circle on the right** of one node
- To the **left side** of the next node
- The line should connect and stay connected

### Problem: "Node shows an error (red X)"

**Troubleshooting**:
1. Click on the node with the error
2. Read the error message (usually very helpful!)
3. Common fixes:
   - Missing required field → Fill in the field
   - Invalid data → Check the data from previous node
   - Connection error → Check credentials

### Problem: "Workflow runs but does nothing"

**Solution**:
- Check each node's output data
- Make sure data is flowing from one node to the next
- Use the "Execute Workflow" button to test step by step

---

## Best Practices

### Do's ✅

1. **Name your workflows clearly**
   - Good: "Daily Sales Report - Email to Team"
   - Bad: "Workflow 1"

2. **Test before activating**
   - Use "Execute Workflow" to test
   - Check each node's output
   - Make sure it does what you expect

3. **Document complex workflows**
   - Add "Sticky Note" nodes with explanations
   - Future you (or your coworkers) will thank you!

4. **Start simple, add complexity**
   - Get the basics working first
   - Then add error handling, notifications, etc.

### Don'ts ❌

1. **Don't activate untested workflows**
   - Always test first!
   - A broken workflow running every hour can cause problems

2. **Don't store passwords in workflow nodes**
   - Use the "Credentials" page instead
   - More secure and reusable

3. **Don't create duplicate workflows**
   - Clone and modify existing workflows
   - Keeps things organized

---

## Quick Reference

| Task | How to Do It |
|------|--------------|
| Create workflow | Workflows → New Workflow |
| Add node | Click + on canvas or on existing node |
| Connect nodes | Drag from right circle to left side of next node |
| Test workflow | Click "Execute Workflow" (top button) |
| Save workflow | Click "Save" (top right) |
| Activate workflow | Toggle switch at top (Inactive → Active) |
| View history | Click "Executions" in sidebar |
| Get help on node | Click node → Look for documentation tab |

---

## Congratulations!

You've created your first N8N workflow! You now know:
- How to add and configure nodes
- How to connect nodes together
- How to test and save workflows
- How to activate automated workflows
- How to view execution history

**You're ready to automate!**

---

## Resources

**Need More Help?**
- **N8N Templates**: Browse real-world examples
- **Documentation**: Click ? in N8N top menu
- **Community**: Ask questions in N8N community forums
- **IT Support**: Contact your administrator

**Want to Learn More?**
- Explore the Templates library
- Try copying and modifying existing workflows
- Experiment with different node types
- Join the N8N community

---

**Remember**: Automation is a skill you build over time. Start simple, practice, and gradually take on more complex workflows. Every expert started exactly where you are now!

---

**Document Version**: 1.0
**Last Updated**: November 8, 2025
**Classification**: Internal Use Only
