#! /usr/bin/env python

from app.app import app


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")