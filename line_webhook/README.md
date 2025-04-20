# [R2GAI] Building AI Agent with Gemini and LINE Messaging API

## LAB3: Connect LINE to Gemini
1. Navigate to the project directory:
   ```bash
   cd 02-connect-line-to-gemini
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
- Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
- Open the `.env` file and update it with your configuration values:
    ```
      LINE_CHANNEL_ID="your_channel_id"
      LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
      LINE_CHANNEL_SECRET=your_channel_secret
      LINE_USER_ID=your_user_id
      GEMINI_API_KEY=your_gemini_api_key
    ```