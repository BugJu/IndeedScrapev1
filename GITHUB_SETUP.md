# Setting Up Your GitHub Repository

This guide will help you connect your local Git repository to GitHub and push your code.

## Step 1: Create a New Repository on GitHub

1. Go to [GitHub](https://github.com/) and sign in to your account.
2. Click on the "+" icon in the top-right corner and select "New repository".
3. Enter "IndeedScrapev1" as the repository name.
4. (Optional) Add a description: "A web scraper for Indeed job listings that extracts programming languages using AI".
5. Choose whether the repository should be public or private.
6. Do NOT initialize the repository with a README, .gitignore, or license as we already have these files locally.
7. Click "Create repository".

## Step 2: Connect Your Local Repository to GitHub

After creating the repository, GitHub will show you commands to connect your existing repository. Use the following commands in your terminal:

```bash
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/IndeedScrapev1.git

# Verify the remote was added correctly
git remote -v

# Push your code to GitHub
git push -u origin master
```

## Step 3: Update Your README.md (Optional)

You may want to update the clone URL in your README.md file to reflect your actual GitHub repository URL:

1. Open README.md
2. Find the line: `git clone https://github.com/yourusername/IndeedScrapev1.git`
3. Replace `yourusername` with your actual GitHub username

## Step 4: Update Git User Information (Optional)

If you want to update the placeholder user information with your actual GitHub information:

```bash
git config user.email "your.actual.email@example.com"
git config user.name "Your Actual Name"
```

## Additional Information

### Using GitHub Desktop (Alternative)

If you prefer a graphical interface:

1. Install [GitHub Desktop](https://desktop.github.com/)
2. Open GitHub Desktop and add your local repository
3. Publish the repository to your GitHub account

### Setting Up GitHub Authentication

If you're prompted for credentials when pushing:

- For HTTPS: Use a personal access token instead of your password
  - Go to GitHub → Settings → Developer settings → Personal access tokens → Generate new token
  - Select the "repo" scope and generate the token
  - Use this token instead of your password when prompted

- For SSH: Set up SSH keys
  - Generate SSH keys: `ssh-keygen -t ed25519 -C "your.email@example.com"`
  - Add the public key to your GitHub account
  - Change the remote URL: `git remote set-url origin git@github.com:YOUR_USERNAME/IndeedScrapev1.git`

### GitHub Actions (Optional)

Consider setting up GitHub Actions for automated testing and deployment:

1. Create a `.github/workflows` directory
2. Add workflow files for CI/CD pipelines

### GitHub Issues and Projects (Optional)

Use GitHub Issues to track bugs and feature requests, and GitHub Projects to organize your work.