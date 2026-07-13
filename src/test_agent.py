from ai.agent import FleetAgent

agent = FleetAgent()

print(
    agent.route(
        "Which drivers made more trips?"
    )
)

print(agent.route("Summarize all trips"))