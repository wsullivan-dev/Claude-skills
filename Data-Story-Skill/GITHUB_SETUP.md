# How to Push to GitHub

Your Data Story Skill repository is ready! Follow these steps to create it on GitHub:

## Method 1: Using GitHub Web Interface (Easiest)

### Step 1: Create Repository on GitHub
1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** button in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `data-story-skill`
   - **Description**: "Transform raw data into compelling narrative reports with visualizations"
   - **Visibility**: Choose Public or Private
   - ⚠️ **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

### Step 2: Push Your Code
GitHub will show you commands. Use these in your terminal:

```bash
# Navigate to your repository directory
cd data-story-repo

# Add the GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/data-story-skill.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push your code
git push -u origin main
```

You'll be prompted for your GitHub credentials. If you have 2FA enabled, you'll need a Personal Access Token instead of your password.

### Step 3: Verify
Visit `https://github.com/YOUR_USERNAME/data-story-skill` to see your repository!

---

## Method 2: Using GitHub CLI (If Installed)

If you have GitHub CLI installed:

```bash
cd data-story-repo

# Login to GitHub (if not already)
gh auth login

# Create repository and push
gh repo create data-story-skill --public --source=. --push

# Or for private:
gh repo create data-story-skill --private --source=. --push
```

---

## Creating a Personal Access Token (if needed)

If you need a Personal Access Token for authentication:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name like "Data Story Skill"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. Copy the token and use it as your password when pushing

---

## After Pushing

### Add Topics/Tags
On your GitHub repository page:
1. Click the ⚙️ gear icon next to "About"
2. Add topics like: `claude-skill`, `data-analysis`, `data-visualization`, `storytelling`, `python`, `pandas`, `matplotlib`

### Enable GitHub Pages (Optional)
To host documentation:
1. Go to Settings → Pages
2. Select branch: `main`
3. Select folder: `/ (root)`
4. Click Save

### Add a Repository Image
1. Click the ⚙️ gear icon next to "About"
2. Upload the Predictive Analytics Partners logo

---

## Updating Your Repository

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

---

## Need Help?

- [GitHub Docs: Creating a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [GitHub Docs: Pushing commits](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
