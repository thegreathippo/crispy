from rules import Event, SubjectProperty


class Action(Event):
    attacker = SubjectProperty("attacker")
    weapon = SubjectProperty("weapon")
    target = SubjectProperty("target")
    cost = 0

    def after(self):
        agent = self.get_subjects()[0]
        if hasattr(agent, "energy"):
            agent.energy -= self.cost
