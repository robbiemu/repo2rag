#!/usr/bin/env python3
from useragent import get_user_agent

def main():
    """Main entry point for the application."""
    print(f'User agent: {get_user_agent()}')

if __name__ == "__main__":
    main()
