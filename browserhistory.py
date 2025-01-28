import json
import datetime
import plotly.graph_objects as go
import plotly.express as px

# Load data
with open('History.json', 'r') as f:
    data = json.load(f)

history = data['Browser History']

# Define categories
categories = {
    "Entertainment": ["youtube", "bilibili", "netflix", "hulu", "primevideo", "disneyplus", "spotify", "pandora", "soundcloud", "twitch", "hbo", "hbonow", "hbomax"],
    "Social Media": ["facebook", "instagram", "twitter", "snapchat", "tiktok", "reddit", "linkedin", "pinterest", "whatsapp", "messenger", "imgur"],
    "Academic": ["canvas", "blackboard", "moodle", "googleclassroom", "khanacademy", "coursera", "udemy", "edx", "udacity", "codecademy", "wikipedia"],
    "Productivity": ["gmail", "outlook", "yahoo", "drive", "onedrive", "dropbox", "slack", "zoom", "microsoftteams", "microsoftword", "microsoftexcel"],
    "Shopping": ["amazon", "ebay", "walmart", "target", "bestbuy", "etsy", "alibaba"],
    "News": ["cnn", "foxnews", "msnbc", "bbc", "npr", "reuters", "apnews", "usatoday", "nytimes", "washingtonpost"],
    "Sports": ["espn", "nfl", "nba", "mlb", "nhl"],
    "Travel": ["expedia", "priceline", "kayak", "orbitz", "hotels", "airbnb"],
    "Health": ["webmd", "mayoclinic", "cdc", "nih", "who"],
    "Food": ["yelp", "grubhub", "doordash", "ubereats", "postmates"],
    "Finance": ["chase", "bankofamerica", "wellsfargo", "citibank", "capitalone"],
    "Gaming": ["steam", "epicgames", "origin", "uplay", "battle.net", "minecraft", "pvp"],
    "Search Engine": ["google", "bing", "yahoo", "duckduckgo", "wikipedia"],
    "Music": ["spotify", "pandora", "soundcloud", "applemusic"],
    "Programming": ["github", "stackoverflow", "w3schools", "geeksforgeeks", "hackerrank", "leetcode"],
    "Adult": ["Pornhub", "Xvideos", "bondage", "boundhub"],
    "AI": ["openai", "deepmind", "poe", "perplexity"],
    "Other": []
}

# Categorize sites
category_sites = {category: [] for category in categories}

def categorize_sites(history, categories, category_sites):
    for site in history:
        matched = False
        for category, urls in categories.items():
            if any(url.lower() in site['url'].lower() for url in urls):
                category_sites[category].append(site['url'])
                matched = True
                break
        if not matched:
            category_sites["Other"].append(site['url'])
    return category_sites

category_sites = categorize_sites(history, categories, category_sites)

# Calculate category counts
category_counts = {category: len(category_sites[category]) for category in category_sites}
sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
cat_labels, cat_sizes = zip(*sorted_categories)

# Calculate most visited sites
def get_most_visited_sites(history):
    most_visited = {}
    for website in history:
        url = website['url'].split("://")[-1].split("/")[0]
        most_visited[url] = most_visited.get(url, 0) + 1
    return sorted(most_visited.items(), key=lambda x: x[1], reverse=True)

sorted_most_visited = get_most_visited_sites(history)
mv_labels, mv_sizes = zip(*sorted_most_visited[:10])

# Calculate date and hour visits
def get_visit_statistics(history):
    date_visits = {}
    hour_visits = {}
    for website in history:
        time_usec = website['time_usec']
        time_sec = time_usec / 1_000_000
        dt = datetime.datetime.fromtimestamp(time_sec)
        date = dt.date()
        hour = dt.hour
        date_visits[date] = date_visits.get(date, 0) + 1
        hour_visits[hour] = hour_visits.get(hour, 0) + 1
    return date_visits, hour_visits

date_visits, hour_visits = get_visit_statistics(history)
dv_labels, dv_sizes = zip(*date_visits.items())
hour_labels, hour_sizes = zip(*hour_visits.items())

# Plotting functions
def create_pie_chart(title, labels, sizes):
    return go.Figure(go.Pie(
        title=title,
        labels=labels, 
        values=sizes,
        marker_colors=px.colors.sample_colorscale("ice", [n/(len(labels) - 1) for n in range(len(labels))]),
        textinfo='label+percent', 
        textposition='inside', 
        insidetextorientation='horizontal', 
        hole=.3
    ))

def create_scatter_plot(title, x, y):
    return px.scatter(
        x=x, y=y,
        title=title,
        labels={"x": title.split()[2], "y": "Visits"},
        color=y
    )

# Create and show plots
freqVisitsPie = create_pie_chart("Most Visited", mv_labels, mv_sizes)
categoryPie = create_pie_chart("Categories", cat_labels, cat_sizes)
dateVisitsScatter = create_scatter_plot("Visits by Date", dv_labels, dv_sizes)
hourVisitsScatter = create_scatter_plot("Visits by Hour", hour_labels, hour_sizes)

# Update layout
freqVisitsPie.update_layout(margin=dict(t=20, l=10, r=10, b=20))
categoryPie.update_layout(margin=dict(t=20, l=10, r=10, b=20))

# Show plots
dateVisitsScatter.show()
hourVisitsScatter.show()
freqVisitsPie.show()
categoryPie.show()
