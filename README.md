# send-photo-aiogram-bot
A Telegram bot developed using aiogram to send photos and manage them through admin menu.

## Getting Started

### 1. Clone the Repository

Clone the repository using the following command:

```bash
git clone https://github.com/nzrsvt/send-photo-aiogram-bot
```

### 2. Navigate to the Repository
Change your directory to the cloned repository:

```bash
cd send-photo-aiogram-bot
```

### 3. Create a Virtual Environment
Create a virtual environment using the following command:

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment
Activate the virtual environment using the appropriate command for your operating system:

On Windows:

```bash
venv\Scripts\activate
```

On Unix/Linux:

```bash
source venv/bin/activate
```

### 5. Install Required Modules
Install the necessary modules for the bot using the following command:

```bash
pip install -r requirements.txt
```

### 6. Configure the Bot
Create a config.py file and set your Telegram bot API token and secret word:

# config.py
```python
API_TOKEN = '' # you can get this token in the @BotFather bot
secret_word = "" # any complex set of characters that can be used to obtain administrator rights
```

### 7. Run the Bot
After completing the above steps, you can start the bot using the provided run_bot.bat file.

**Now your bot should be up and running! Enjoy using the Send Photo Aiogram Bot.**
