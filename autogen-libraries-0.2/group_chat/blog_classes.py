class Blog:
    def __init__(self, title, introduction, problem_deep_dive, why_solution_needed, solution):
        self.title = title
        self.introduction = introduction
        self.problem_deep_dive = problem_deep_dive
        self.why_solution_needed = why_solution_needed
        self.solution = solution

    def to_dict(self):
        return {
            "title": self.title.to_dict(),
            "introduction": self.introduction.to_dict(),
            "problem_deep_dive": self.problem_deep_dive.to_dict(),
            "why_solution_needed": self.why_solution_needed.to_dict(),
            "solution": self.solution.to_dict(),
        }

class Title:
    def __init__(self, title):
        self.title = title

    def to_dict(self):
        return {"title": self.title}

class Introduction:
    def __init__(self, hook, problem_statement, article_overview):
        self.hook = hook
        self.problem_statement = problem_statement
        self.article_overview = article_overview

    def to_dict(self):
        return {
            "hook": self.hook,
            "problem_statement": self.problem_statement,
            "article_overview": self.article_overview,
        }

class ProblemDeepDive:
    def __init__(self, problem_deep_dive, impact, target_audience):
        self.problem_deep_dive = problem_deep_dive
        self.impact = impact
        self.target_audience = target_audience

    def to_dict(self):
        return {
            "problem_deep_dive": self.problem_deep_dive,
            "impact": self.impact,
            "target_audience": self.target_audience,
        }

class WhySolutionNeeded:
    def __init__(self, rationale, benefits_goals):
        self.rationale = rationale
        self.benefits_goals = benefits_goals

    def to_dict(self):
        return {
            "rationale": self.rationale,
            "benefits_goals": self.benefits_goals,
        }

class Solution:
    def __init__(self, proposed_solution, implementation_details, technical_breakdown, use_cases):
        self.proposed_solution = proposed_solution
        self.implementation_details = implementation_details
        self.technical_breakdown = technical_breakdown
        self.use_cases = use_cases

    def to_dict(self):
        return {
            "proposed_solution": self.proposed_solution,
            "implementation_details": self.implementation_details,
            "technical_breakdown": self.technical_breakdown,
            "use_cases": self.use_cases,
        }