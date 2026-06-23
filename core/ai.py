import ollama
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from tavily import TavilyClient

class ChatEngine:
    def __init__(self):
        self.model = "phi3:mini"
        self.history = [
            {
                "role": "system",
                "content": """
        You are NEXUS AI.

        You are a modern real-time assistant.

        Never mention:
        - knowledge cutoff
        - training data
        - outdated information

        If live data is provided, treat it as current truth.

        Keep answers short and direct.
        """
            }
        ]
        self.tavily = TavilyClient(
            api_key="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"
        )

        self.news_key = "2ae04e3e020947a6a9e78720126c7e3d"

        self.cricket_key = "7da593ae-e536-4d41-921b-3c6bead1b54f"

    def get_date(self):
        return datetime.now().strftime("%d %B %Y")
    
    def get_month(self):
        return datetime.now().strftime("%B")

    def get_time(self):
        return datetime.now().strftime("%I:%M %p")
    
    def chat(self, user_message):
        query = user_message.lower()
        # Date & Time
        if "date" in query:
            return f"Today's date is {self.get_date()}"

        if "time" in query:
            return f"Current time is {self.get_time()}"

        if "month" in query:
            return f"Current month is {self.get_month()}"

# IPL
        if "ipl" in query or "cricket" in query:
            return self.get_live_ipl()

# News
        if "news" in query:
            return self.get_news()

# Current Affairs / Leaders
        if any(word in query for word in [
            "chief minister",
            "prime minister",
            "president",
            "governor",
            "current leader"
            ]):
                result = self.live_search(user_message)

                if result:
                    return result

# Everything else -> Ollama
        return self.ask_ollama(user_message)

    def ask_ollama(self, user_message):
        self.history.append({
            "role": "user",
            "content": user_message
        })
        response = ollama.chat(
            model=self.model,
            messages=self.history
        )
        reply = response["message"]["content"]
        self.history.append({
            "role": "assistant",
            "content": reply
        })
        return reply 
       

    def clear_history(self):
        self.history = []

    
    def internet_search(self, query):
        try:
            if "ipl" in query.lower() or "cricket" in query.lower():
                url = "https://www.cricbuzz.com/cricket-match/live-scores"

            else:

                url = "https://duckduckgo.com/html/"

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers)

            soup = BeautifulSoup(response.text, "html.parser")

            text = soup.get_text(separator="\n")

            return text[:3000]

        except Exception as e:

            print("Search Error:", e)

            return None
    
    def get_news(self):
        url = (
            "https://newsapi.org/v2/top-headlines"
            f"?country=in&apiKey={self.news_key}"
        )
        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        news = []

        for article in data["articles"][:5]:

            news.append(
                f"• {article['title']}"
            )

        return "\n".join(news)
    
    
    def get_live_ipl(self):
        url = (
            "https://api.cricketdata.org/v1/currentMatches"
            f"?apikey={self.cricket_key}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        matches = []

        for match in data.get("data", []):

            matches.append(
                f"{match['name']}\n"
                f"Status: {match['status']}\n"
            )

        if matches:
            return "\n\n".join(matches)

        return "No live IPL match found."
    
    def live_search(self, query):
        result = self.tavily.search(
            query=query,
            max_results=3
        )

        answers = []

        for item in result["results"]:

            answers.append(
                item["content"]
            )

        return "\n".join(answers)