# MailPhish

Open-source, self-hosted phishing awareness training for teams. MailPhish is designed to help small organizations understand how participants respond to links in simulated emails and teach them to recognize warning signs.

## Project status

MailPhish is in early development. The current starter serves a local web page that checks its connection to the FastAPI backend.

## Planned prototype

1. An administrator creates a training exercise and selects a fictional email scenario.
2. Participants view the sample messages in a local test inbox using fictional accounts.
3. An educational page explains the warning signs and how to report a suspicious email.
4. The administrator can revisit past exercises and see aggregate counts for test messages, exercise link opens, and completed activities.

The prototype is scoped to a controlled training environment. AI can help draft educational explanations, which the team reviews before adding them to the scenario library.

## Repository layout

| Directory | Planned contents |
| --- | --- |
| [`backend/app/`](backend/app/) | Python and FastAPI application for exercises, scenarios, and aggregate results |
| [`frontend/src/`](frontend/src/) | Administrative views and participant learning pages. The frontend framework is open for discussion. |
| [`templates/emails/`](templates/emails/) | HTML bodies for fictional training examples |

The proposed local setup uses Docker Compose, SQLite, and a local test inbox.

## Run the development starter

Use Python 3.11 or newer. Follow the [development guide](docs/development.md) to create a virtual environment and install dependencies with `pip`. Then run this from the repository root with the environment active.

```sh
fastapi dev
```

Open [MailPhish](http://127.0.0.1:8000/) or [Swagger UI](http://127.0.0.1:8000/docs).

## Contributing

Ideas, documentation improvements, and feedback on the prototype are welcome. Open an [issue](https://github.com/mailphish/mailphish/issues) to discuss a change, or submit a pull request for small, focused improvements. Use fictional data in examples and screenshots.

## License

MailPhish is released under the [MIT License](LICENSE).
