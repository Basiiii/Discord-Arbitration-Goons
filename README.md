# Warframe Arbitration Notifier Discord Bot

## Overview

The Warframe Arbitration Notifier Discord Bot is a private tool designed to keep Warframe players informed about new arbitration missions in real-time.

This Discord bot utilizes a sophisticated backend process to fetch and deliver timely information to a designated Discord channel in a public server with thousands of Arbitration players. The discord server is available [here](https://discord.gg/arbitrations).

## Why This Project?

The inception of this project stems from the shortcomings of an existing public API used to fetch real-time data on Warframe arbitration missions. The public API proved inconsistent, slow, and often skipped missions. In response, this project was initiated to address these limitations and create a more accurate and responsive solution. The custom API developed for this bot directly interacts with the Warframe game, ensuring reliability and publishing new alerts within one minute of their availability in-game.

## How It Works

The core functionality of the Warframe Arbitration Notifier Discord Bot revolves around a proprietary scanner, a custom API developed explicitly for this project. This scanner directly interacts with the Warframe game, parsing real-time data on arbitration missions and ensuring accuracy and reliability. The details of this custom scanning process are proprietary and cannot be shared.

In the event that our proprietary scanner encounters rare downtimes (which account for only 0.1% of the time, given our 99.9% uptime), the bot seamlessly switches to a public API as a backup. This external API is used to fetch real-time data on arbitration missions, providing continuity in mission alerts even during exceptional circumstances.

Additionally, another mechanism involves scanning JSON files generated from a private parser. This parser interacts with the Warframe game to extract relevant information, which is then formatted into JSON files. These files serve as an alternative data source for the Discord bot.

The Discord bot, showcased in this repository, acts as the frontend for this versatile data retrieval process. Here's how it functions:

1. **Data Fetching:**
   - The bot primarily fetches information from our proprietary scanner but seamlessly switches to the public API in case of rare downtimes.

2. **Data Preparation:**
   - The retrieved data is processed and prepared for presentation in a Discord embed. This includes essential details about new arbitration missions.

3. **Notification Publishing:**
   - The bot automatically publishes notifications to a designated Discord channel in a public server with thousands of Arbitration players. This ensures that the information is promptly available for anyone following the channel, enhancing the overall gaming experience for Warframe enthusiasts.

## Showcase

This repository is made public to showcase coding skills and project structure. It is not intended for general use or deployment.

### Key Features

- **Real-time Notifications:** Receive instant alerts for new arbitration missions.
- **Discord Integration:** Running on a Discord bot, anyone can easily get notifications for new arbitration missions.

### Project Structure

The project is structured to ensure modularity, scalability, and maintainability. Key components include:

- **API Scanner Module:** Handles interactions with the public API and proprietary scanner.
- **Data Processing Module:** Responsible for preparing fetched data for presentation in Discord embeds.
- **Notification Module:** Manages the publishing of notifications to the designated Discord channel.
- **Configuration Management:** Centralized configuration files for easy setup and customization.

Explore the code to understand the underlying architecture and implementation details.

## License

All rights reserved. This repository and its contents are proprietary and may not be reproduced, modified, or distributed without explicit permission from the owner.

© [Enrique R.](https://github.com/Basiiii)

For inquiries and permissions, please contact the owner: `basigraphics@gmail.com`
