#!/usr/bin/env python
"""Dashboard for Libre Solar box. Reads data from sqlite database
and plots live data at http://localhost:8050"""

from website.live_dashboard import create_app

app = create_app()

if __name__ == '__main__':
    app.run_server(debug=True)
