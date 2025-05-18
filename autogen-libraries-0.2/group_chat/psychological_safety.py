from blog_classes import Blog, Title, Introduction, ProblemDeepDive, WhySolutionNeeded, Solution

title = Title("The Importance of Psychological Safety in Technical Scrum Teams")

introduction = Introduction(
    hook="""Imagine you enter a team meeting and you find silence in the room. 
            No one is speaking up, not much sharing of ideas are happening. 
            There are no conflicts per se and there is no difference in opinion.
            The team seems to be working in harmony but there is no innovation, no new ideas.
            There is one or two people only speaking and everyone follows them. 
            Nobody is asking questions or challenging the status quo.
            Nobody is questioning why they are doing what they are doing.""",
    problem_statement="""This is a common problem of lack of psychological safety in teams.
            Psychological safety is the belief that one will not be punished or humiliated for speaking up with ideas, 
            questions, concerns or mistakes. It is the foundation of a high performing team.
            Lack of psychological safety leads to lack of innovation, lack of creativity, lack of diversity of thought, 
            lack of engagement and lack of motivation. It leads to groupthink, lack of trust and lack of collaboration.
            It leads to fear of failure, fear of speaking up, fear of being judged and fear of being ridiculed.
            Moreover, it means there is a lack of empowerment in teams, lack of ownership and lack of accountability.
            Because the team does not know their end goal. They are acting on what is being told them to do and maybe 
            even how to do something. Without their own opinions and ideas being heard.""",
    article_overview="""In this article, I intend to talk about the importance of psychological safety in teams.
            What is it and why it is important. 
            I will talk about the problem of lack of psychological safety in teams.
            What are the consequences of it.
            Who is affected by it.
            Why it is important to cultivate a high sense of safety in the team towards expressing their thoughts and ideas.
            I will also talk about how it can be achieved.
            What are the strategies and best practices to cultivate psychological safety in teams.
            And then how it can be measured. Since if something cannot be measured it cannot be improved."""
)

problem_deep_dive = ProblemDeepDive(
    problem_deep_dive="""As explained in introduction, psychological safety is the belief 
                         that one will not be punished or humiliated for speaking up with ideas, 
                         questions, concerns or mistakes. 
                         It is the foundation of a high performing team. 
                         Lack of psychological safety leads to lack of innovation, lack of creativity, 
                         lack of diversity of thought, lack of engagement and lack of motivation. 
                         It leads to groupthink, lack of trust and lack of collaboration. 
                         It leads to fear of failure, fear of speaking up, fear of being judged 
                         and fear of being ridiculed. 
                         Moreover, it means there is a lack of empowerment in teams, lack of ownership and 
                         lack of accountability. 
                         Because the team does not know their end goal. They are acting on what is 
                         being told them to do and maybe even how to do something. 
                         Without their own opinions and ideas being heard.
                         The real outcome of a team is team work which comes through collaboration. 
                         Its not the individual work that makes a team successful.
                         Its the collective work of the team that makes it successful.
                         When ideas are shared, when there is a healthy debate, when there is a
                         healthy conflict, when there is a healthy disagreement, when there is a
                            healthy discussion, when there is a healthy brainstorming. then good solutions come out. 
                     """,
    impact= """Consequences of having psychologically unsafe environment is many. 
               with lack of sharing of ideas, lack of innovation, lack of creativity, lack of diversity of thought,
               leads to lack of engagement and lack of motivation. Team does not have ownership and accountability. 
                They are not empowered to make decisions. They are not empowered to take risks.
                A team that is established as cross-functional and cross-skilled need to collaborate to create 
                right solutions. And that whole purpose is gone down. In a team 1+1 is not 2 its 11. and loss of this
                synergy is a loss to businesses.
                There is intense competition in market for businesses to survive and thrive. Lack of psychological safety
                would put you behind in this competition and can lead to losses in millions of dollars of not being able 
                to harness energy of your teams.     
            """,
    target_audience="Target Audience for this is engineering leaders managing technical scrum teams."
)

why_solution_needed = WhySolutionNeeded(
    rationale=""" Teams should be vibrant in energy and motivation. 
                  Teams must innovate and compete in the market.
                  Teams must be creative and diverse in thought for business success.
                  it leads to retention of employees, it leads to better customer satisfaction,
                  it leads to better products and services, it leads to better team work and collaboration.
                  it leads to better employee satisfaction also. 
                """,
    benefits_goals="""Happy teams innovating and building features that delight customers .
                    leaders supporting and guiding teams to success.
                    Teams are independent and require less supervision.
                    Teams are motivated and engaged in their work.
                    more profits, retention, customer satisfaction, market leadership and business growth.
                    """
)

solution = Solution(
    proposed_solution="Explain the solution in detail, including strategies and best practices.",
    implementation_details="Explain the steps involved in implementing the solution.",
    technical_breakdown="Provides in-depth technical breakdown explanations.",
    use_cases="Provides use cases."
)

blog = Blog(
    title=title,
    introduction=introduction,
    problem_deep_dive=problem_deep_dive,
    why_solution_needed=why_solution_needed,
    solution=solution
)