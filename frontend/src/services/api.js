import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

/**
 * Analyze a legal case.
 * @param {string} caseDescription - The case description text
 * @param {File[]} files - Optional array of File objects to upload
 * @returns {Promise} Analysis results from all AI modules
 */
export async function analyzeCase(caseDescription, files = []) {
  const formData = new FormData();
  formData.append('case_description', caseDescription);

  if (files && files.length > 0) {
    files.forEach((file) => {
      formData.append('documents', file);
    });
  }

  const response = await api.post('/analyze-case', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
}

/**
 * Get the download URL for a PDF checklist.
 * @param {string} filename - The PDF filename from analysis results
 * @returns {string} Full download URL
 */
export function getChecklistDownloadUrl(filename) {
  return `${API_BASE_URL}/download-checklist/${filename}`;
}

/**
 * Health check
 */
export async function healthCheck() {
  const response = await api.get('/health');
  return response.data;
}

export default api;
