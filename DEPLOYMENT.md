# FLAVYR MVP - Streamlit Cloud Deployment Guide

## Quick Deploy

This application is ready for deployment on Streamlit Community Cloud. Follow these steps:

### Prerequisites

1. GitHub account
2. Streamlit Community Cloud account (free at https://share.streamlit.io)
3. This repository pushed to GitHub

### Deployment Steps

1. **Go to Streamlit Community Cloud**
   - Visit https://share.streamlit.io
   - Sign in with your GitHub account

2. **Deploy New App**
   - Click "New app" button
   - Select your GitHub repository: `njpastrone/flavyr-mvp`
   - Main file path: `app.py`
   - App URL: Choose your preferred subdomain

3. **Deploy**
   - Click "Deploy!" button
   - Wait 2-3 minutes for initial deployment
   - Your app will be live at `https://[your-subdomain].streamlit.app`

## Configuration Files

The following files have been configured for Streamlit Cloud:

### `.streamlit/config.toml`
- Theme settings (colors, fonts)
- Server configuration (headless mode, CORS)
- Upload size limit (200MB for large CSV files)
- Usage stats disabled for privacy

### `requirements.txt`
- Pinned versions for reproducibility:
  - `streamlit==1.28.0`
  - `pandas==2.0.3`
  - `plotly==5.17.0`
  - `fpdf2==2.7.6`

### `packages.txt`
- System-level dependencies (currently none needed)
- Placeholder file for future system packages

## Database Handling

The app automatically detects Streamlit Cloud environment and adjusts:

**Local Development:**
- Database stored in `database/flavyr.db`
- Persists between sessions

**Streamlit Cloud:**
- Database stored in `/tmp/flavyr.db`
- Ephemeral storage (resets on restart)
- Benchmark data automatically reloaded on startup
- User uploads persist only during session

This design is intentional for the MVP:
- No user data stored permanently (privacy)
- Fresh environment on each deployment
- Benchmark data always available

## Environment Variables

No environment variables required for basic deployment.

Optional for future enhancements:
- `STREAMLIT_SHARING_MODE=1` - Auto-detected by platform
- `STREAMLIT_CLOUD=1` - Auto-detected by platform

## Testing Before Deployment

Test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# Open browser to http://localhost:8501
```

## Post-Deployment Checks

After deployment, verify:

1. **Home Page Loads**
   - Should see welcome message and getting started guide

2. **Data Upload Works**
   - Navigate to "Transaction Insights" tab
   - Upload `data/sample_transaction_data.csv`
   - Select restaurant type
   - Click "Analyze Transactions & Generate Insights"

3. **Dashboard Displays**
   - Check performance grade shows
   - Verify KPI metrics display correctly
   - Confirm charts render properly

4. **Recommendations Generate**
   - Should see prioritized recommendations
   - Transparency sections expand correctly
   - Confidence indicators display

5. **Report Export Works**
   - PDF download functions
   - HTML export functions

## Troubleshooting

### App Won't Start
- Check Streamlit Cloud logs for errors
- Verify all files in repository (especially `data/` folder)
- Confirm requirements.txt has correct syntax

### Database Errors
- Normal on first load - database auto-creates
- Check that benchmark CSV files exist in `data/` folder
- Verify no syntax errors in data_loader.py

### Upload Issues
- Verify file size under 200MB
- Check CSV format matches expected columns
- Review validation error messages in app

### Missing Data
- Ensure all files in `data/` folder are committed to Git
- Check .gitignore doesn't exclude necessary files
- Verify CSV files have correct headers

## Performance Optimization

For production deployment:

1. **Caching**
   - Already implemented with `@st.cache_data`
   - Benchmark data cached after first load
   - Analysis results cached per session

2. **File Size**
   - Keep sample CSVs under 5MB
   - Users can upload larger files (up to 200MB)

3. **Memory Management**
   - SQLite database in /tmp is lightweight
   - Session state properly managed
   - No memory leaks in current implementation

## Security Considerations

Current setup:
- XSRF protection enabled
- No external API calls
- All data processing local to app
- No permanent data storage on cloud
- CORS disabled (not needed)

For production with real customer data:
- Consider encrypted database
- Add authentication layer
- Implement access controls
- Enable audit logging

## Updating the Deployment

To update the live app:

```bash
# Make changes locally
# Test thoroughly

# Commit and push to GitHub
git add .
git commit -m "Update message"
git push origin main

# Streamlit Cloud auto-deploys from main branch
# Wait 2-3 minutes for changes to go live
```

## Custom Domain (Optional)

Streamlit Cloud Pro allows custom domains:
1. Upgrade to Pro plan
2. Configure DNS CNAME record
3. Add custom domain in Streamlit Cloud settings
4. SSL certificate auto-provisioned

## Monitoring

Streamlit Cloud provides:
- Real-time logs
- Resource usage metrics
- Error tracking
- Deployment history

Access via the Streamlit Cloud dashboard.

## Limits (Community Cloud)

Free tier includes:
- 1 GB RAM per app
- 1 CPU per app
- Unlimited apps (public repos)
- No usage limits
- Auto-sleep after inactivity

Sufficient for FLAVYR MVP with 5-10 concurrent users.

## Support

If issues arise:
- Check Streamlit Cloud documentation: https://docs.streamlit.io/streamlit-community-cloud
- Review logs in Streamlit Cloud dashboard
- GitHub issues: https://github.com/njpastrone/flavyr-mvp/issues
- Streamlit Community Forum: https://discuss.streamlit.io

## Next Steps After Deployment

1. **Share URL** with pilot restaurants
2. **Monitor usage** via Streamlit Cloud dashboard
3. **Collect feedback** from users
4. **Iterate** based on real-world usage
5. **Plan Phase 2** features

Your FLAVYR MVP is now live and ready for pilot testing!
