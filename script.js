// API Key configuration
const API_KEY = 'your-secret-api-key-here'; // Replace with your actual API key

async function generateBrand() {
  const keyword = document.getElementById('keyword').value;
  if (!keyword) {
    alert('Please enter a business idea');
    return;
  }

  const response = await fetch(`/generate-names?keyword=${encodeURIComponent(keyword)}`, {
    headers: {
      'X-API-Key': API_KEY
    }
  });
  const data = await response.json();

  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '<h3>Generated Brand Names & Strategy:</h3><div style="display: grid; gap: 20px;">' +
    data.brands.map(item => `
      <div style="padding: 15px; border-left: 5px solid #2575fc; background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%); border-radius: 8px; box-shadow: 0 2px 8px rgba(37, 117, 252, 0.1);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
          <strong style="font-size: 22px; color: #2575fc;">${item.name}</strong>
          <span style="font-size: 12px; background: #2575fc; color: white; padding: 4px 10px; border-radius: 20px;">${item.personality.split(',')[0].trim()}</span>
        </div>
        <p style="font-size: 14px; color: #666; margin: 8px 0; font-style: italic;">"${item.tagline}"</p>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 12px;">
          <div>
            <strong style="font-size: 11px; color: #2575fc; text-transform: uppercase;">Target Audience</strong>
            <p style="font-size: 13px; color: #555; margin: 4px 0;">${item.audience}</p>
          </div>
          <div>
            <strong style="font-size: 11px; color: #2575fc; text-transform: uppercase;">Brand Positioning</strong>
            <p style="font-size: 13px; color: #555; margin: 4px 0;">${item.positioning}</p>
          </div>
          <div>
            <strong style="font-size: 11px; color: #2575fc; text-transform: uppercase;">Social Handles</strong>
            <p style="font-size: 12px; color: #666; margin: 4px 0; font-family: monospace; background: white; padding: 6px; border-radius: 4px;">${item.social_handles}</p>
          </div>
          <div>
            <strong style="font-size: 11px; color: #2575fc; text-transform: uppercase;">Domain Options</strong>
            <p style="font-size: 12px; color: #666; margin: 4px 0; font-family: monospace; background: white; padding: 6px; border-radius: 4px;">${item.domains}</p>
          </div>
        </div>
      </div>
    `).join('') +
    '</div>';
}

async function generateBrandNames() {
  const keyword = document.getElementById('brand-keyword').value;
  if (!keyword) {
    alert('Please enter a business idea');
    return;
  }

  const response = await fetch(`/generate-names?keyword=${encodeURIComponent(keyword)}`, {
    headers: {
      'X-API-Key': API_KEY
    }
  });
  const data = await response.json();

  const resultsDiv = document.getElementById('brand-results');
  resultsDiv.innerHTML = '<h3>Generated Brand Names & Taglines:</h3><div style="display: grid; gap: 15px;">' +
    data.brands.map(item => `<div style="padding: 12px; border-left: 4px solid #2575fc; background: #f8f9fa; border-radius: 4px;"><strong style="font-size: 18px; color: #2575fc;">${item.name}</strong><br/><em style="font-size: 13px; color: #666; margin-top: 5px; display: block;">❝${item.tagline}❞</em></div>`).join('') +
    '</div>';
}

async function generateLogo() {
  const keyword = document.getElementById('logo-keyword').value;
  if (!keyword) {
    alert('Please enter a brand name');
    return;
  }

  const response = await fetch(`/generate-logo?keyword=${encodeURIComponent(keyword)}`, {
    headers: {
      'X-API-Key': API_KEY
    }
  });

  if (!response.ok) {
    const errorMsg = await response.text();
    alert('Logo API error: ' + errorMsg);
    return;
  }

  const data = await response.json();

  const resultsDiv = document.getElementById('logo-result');
  resultsDiv.innerHTML = '<h3>Generated Logo Variants:</h3>' +
    '<div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">' +
    data.logos.map(logo => `
      <div style="padding: 10px; background: rgba(255,255,255,0.85); border-radius: 12px; width: 320px; box-shadow: 0 6px 20px rgba(0,0,0,0.12);">
        <h4 style="font-family: 'Segoe UI', sans-serif; font-size: 16px; color: #1D4ED8; text-align:center; margin: 8px 0;">${logo.style}</h4>
        ${logo.svg}
      </div>
    `).join('') +
    '</div>';
}

async function generateMarketing() {
  const keyword = document.getElementById('marketing-keyword').value;
  if (!keyword) {
    alert('Please enter a product/service');
    return;
  }

  const response = await fetch(`/generate-marketing?keyword=${encodeURIComponent(keyword)}`, {
    headers: {
      'X-API-Key': API_KEY
    }
  });
  const data = await response.json();

  const resultsDiv = document.getElementById('marketing-results');
  resultsDiv.innerHTML = '<h3>Marketing Ideas:</h3><ul>' +
    data.ideas.map(idea => `<li>${idea}</li>`).join('') +
    '</ul>';
}

// Add Enter key functionality to input fields
document.addEventListener('DOMContentLoaded', function() {
  // Main brand generator input
  const keywordInput = document.getElementById('keyword');
  if (keywordInput) {
    keywordInput.addEventListener('keypress', function(event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        generateBrand();
      }
    });
  }

  // Logo generator input
  const logoKeywordInput = document.getElementById('logo-keyword');
  if (logoKeywordInput) {
    logoKeywordInput.addEventListener('keypress', function(event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        generateLogo();
      }
    });
  }

  // Brand names generator input
  const brandKeywordInput = document.getElementById('brand-keyword');
  if (brandKeywordInput) {
    brandKeywordInput.addEventListener('keypress', function(event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        generateBrandNames();
      }
    });
  }

  // Marketing ideas generator input
  const marketingKeywordInput = document.getElementById('marketing-keyword');
  if (marketingKeywordInput) {
    marketingKeywordInput.addEventListener('keypress', function(event) {
      if (event.key === 'Enter') {
        event.preventDefault();
        generateMarketing();
      }
    });
  }
});
