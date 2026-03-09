# BrandCraft AI - API Key Setup Guide

## 🔐 API Key Authentication

Your BrandCraft AI application now includes API key authentication to protect your endpoints.

### Setup Instructions

1. **Generate a Secure API Key:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Update the .env file:**
   - Open `.env` in your project directory
   - Replace `your-secret-api-key-here` with your generated key
   - Example: `BRANDCRAFT_API_KEY=abc123def456...`

3. **Update script.js:**
   - Open `script.js`
   - Replace `'your-secret-api-key-here'` with your actual API key
   - The constant is at the top of the file: `const API_KEY = 'your-key-here';`

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Restart the Server:**
   ```bash
   python app.py
   ```

### API Endpoints

All generation endpoints now require API key authentication:

- `GET /generate-logo?keyword=<brand_name>`
- `GET /generate-names?keyword=<business_idea>`
- `GET /generate-marketing?keyword=<product_service>`

### Authentication Methods

You can provide the API key in two ways:

1. **Header:** `X-API-Key: your-api-key-here`
2. **Query Parameter:** `?api_key=your-api-key-here`

### Testing

**Without API Key (should fail):**
```bash
curl "http://localhost:3000/generate-names?keyword=tech"
# Returns: {"error": "Invalid or missing API key"}
```

**With API Key (should work):**
```bash
curl -H "X-API-Key: your-api-key-here" "http://localhost:3000/generate-names?keyword=tech"
# Returns: JSON with brand data
```

### Security Notes

- Keep your API key secure and never commit it to version control
- Use environment variables in production
- Consider rotating keys periodically
- The default key in the code is just a placeholder - replace it immediately

### Environment Variables

The application loads configuration from a `.env` file:
- `BRANDCRAFT_API_KEY`: Your API key for authentication

Make sure to add `.env` to your `.gitignore` file to prevent accidental commits.