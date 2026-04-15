# 🚌 SmartBus AI: Bengaluru Smart Transit System

SmartBus AI is a Python-based web application designed to simplify public transit navigation in Bengaluru. By leveraging BMTC (Bangalore Metropolitan Transport Corporation) datasets, the platform allows users to visualize complete route flows, identify intermediate stops, and see clear origin-to-destination mapping.

## 🚀 Key Features

- **Route Lookup:** Search for any BMTC bus number (e.g., 500C, 242-LA, G-3) to retrieve its full path.
- **Dynamic Route Flow:** A visual vertical timeline showing every stop from origin to destination with clear color-coding (Green for Start, Red for End).
- **Route Variants:** Handles multiple variants of the same bus number, displaying them as distinct options.
- **Modern UI:** A dark-themed, responsive interface built with a focus on usability and mobile-first design.

## 🛠️ Technical Stack

- **Backend:** Python, Flask
- **Data Processing:** Pandas (supporting both `.csv` and `.xlsx` datasets)
- **Frontend:** HTML5, CSS3 (Custom Syne & DM Sans typography), Vanilla JavaScript
- **Deployment Ready:** Configured for local development with simple Flask entry points

## 📋 Prerequisites

Before running the project, ensure you have the following:
- Python 3.x installed
- The BMTC dataset file named `bmtc_routes_with_stops.csv` in the root directory

## 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/MSK2308SA/smartbusAI.git](https://github.com/MSK2308SA/smartbusAI.git)
   cd smartbusAI
