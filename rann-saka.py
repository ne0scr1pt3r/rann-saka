"""
Project: Rann-Saka
Description: A comprehensive tool for evaluating unfounded allegations in the Cybersecurity domain.
Author: ne0scr1pt3r
Date: January 1, 2024
License: MIT License
Version: 1.0.0

MIT License

Copyright (c) 2024 ne0scr1pt3r

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
import os
import sys
import textwrap

current_time = time.ctime()


# Indicators for general evaluation
def evaluate_general_indicators(base_tier_weights):
    indicators = {
        "Consistent negative feedback\n(Frequent negative feedback, "
        "regardless of performance or improvement)": (False, 3, 1.2),

        "Contradictory information\n(Receiving conflicting instructions or "
        "feedback)": (False, 3, 1.1),

        "Vague or non-specific criticism\n(Criticism that lacks clear and "
        "actionable points)": (False, 2, 1.0),

        "Personal rather than professional feedback\n(Feedback focuses on "
        "personal traits rather than professional skills)": (False, 2, 1.0),

        "Lack of credibility\n(Feedback or instructions lack grounding in "
        "facts or reality)": (False, 3, 1.1),

        "Unusual communication from prospective employers\n(Unexpected or "
        "unconventional communication styles from potential employers)":
        (False, 1, 0.9),

        "Decline in job offers\n(Noticeable decrease in job offers or "
        "opportunities)": (False, 3, 1.4),

        "Direct warnings\n(Explicit warnings about performance or behavior)":
        (False, 3, 1.2),

        "Legal action threats\n(Threats of legal action in response to "
        "actions or performance)": (False, 3, 1.3),

        "Inconsistencies over time\n(Feedback or expectations that change "
        "unpredictably over time)": (False, 2, 1.0),

        "Contradiction with documented facts\n(Feedback or claims that "
        "contradict documented evidence)": (False, 3, 1.2),

        "Unverifiable or exaggerated claims\n(Claims or accusations that "
        "cannot be substantiated)": (False, 2, 1.0),

        "Discrepancy with colleague feedback\n(Significant differences "
        "between feedback from different colleagues)": (False, 2, 0.9),

        "Unwillingness to provide details\n(Reluctance to give detailed "
        "information or clarification)": (False, 1, 0.8),

        "Feedback based on rumor or speculation\n(Feedback that is not "
        "based on direct observation or evidence)": (False, 2, 0.9),

        "Negative feedback on areas outside of their oversight\n(Criticism "
        "about aspects outside the employee's control or responsibility)":
        (False, 1, 0.7),

        "Timing of the accusations or feedback\n(Feedback timing that may "
        "have ulterior motives or context)": (False, 1, 0.8),

        "Impact on career opportunities\n(Feedback that adversely affects "
        "future career prospects)": (False, 3, 1.1),

        "Response to clarification requests\n(How feedback providers respond "
        "to requests for clarification)": (False, 2, 0.9),

        "Unconstructive feedback\n(Feedback that doesn't offer a clear path "
        "to improvement)": (False, 2, 1.0),

        "Frequent criticism\n(Regular and persistent criticism)":
        (False, 1, 0.9),

        "Inconsistency\n(Lack of consistency in feedback or expectations)":
        (False, 2, 1.0),

        "Personal, not professional\n(Focus on personal attributes rather "
        "than professional performance)": (False, 2, 1.0),

        "Public criticism\n(Criticism delivered in a public setting)":
        (False, 1, 0.8),

        "No recognition of improvement\n(Ignoring or not acknowledging "
        "improvements made)": (False, 2, 0.9),

        "Comparisons with others\n(Unfavorable comparisons with other "
        "colleagues)": (False, 1, 0.7),

        "Ignoring context\n(Overlooking the context or circumstances of "
        "actions or performance)": (False, 2, 0.9),

        "Lack of support\n(Insufficient support or resources for the role)":
        (False, 1, 0.8),

        "Impact on morale\n(Feedback that negatively affects morale)":
        (False, 2, 0.9),

        "Excessive focus on minor errors\n(Overemphasis on small mistakes)":
        (False, 2, 0.9),

        "Lack of objective evidence\n(Feedback not supported by objective "
        "facts or data)": (False, 2, 1.0),

        "Feedback contrary to previous evaluations\n(Feedback that "
        "contradicts earlier evaluations)": (False, 3, 1.2),

        "Isolation from collaborative opportunities\n(Exclusion from "
        "opportunities for teamwork and collaboration)": (False, 1, 0.8),

        "Exclusion from professional development\n(Being left out of "
        "professional growth and development opportunities)":
        (False, 1, 0.7)
    }

    # Iterating general indicators for answers
    max_length = max(len(indicator) for indicator in indicators.keys())
    print('-' * max_length)
    print("Please answer the following questions with 'yes'(y) or 'no'(n) or 'exit':\n")
    for indicator in indicators.keys():
        while True:
            response = input(f"{indicator}: ").strip().lower()
            if response in ['yes', 'y']:
                indicators[indicator] = (True, indicators[indicator][1], indicators[indicator][2])
                break
            elif response in ['no', 'n']:
                indicators[indicator] = (False, indicators[indicator][1], indicators[indicator][2])
                break
            elif response == 'exit':
                print("Program exited by user.")
                sys.exit()
            else:
                print("Invalid input. Please answer with 'yes'(y) or 'no'(n) or 'exit'.")
        print("-" * max_length)

    weighted_sum, weighted_percentage = calculate_hybrid_score(indicators, base_tier_weights)
    true_indicators_tier_1 = sum(1 for value, tier, _ in indicators.values()
                                 if value and tier == 1)
    true_indicators_tier_2 = sum(1 for value, tier, _ in indicators.values()
                                 if value and tier == 2)
    true_indicators_tier_3 = sum(1 for value, tier, _ in indicators.values()
                                 if value and tier == 3)
    # Summary
    total_indicators = len(indicators)
    true_indicators = sum(1 for value, _, _ in indicators.values() if value)
    summary = (
        "- Indicator Analysis:\n"
        f"    Out of a total of {total_indicators} indicators analyzed, {true_indicators} "
        f"(or {weighted_percentage:.2f}% of the maximum possible score) were identified as true. "
        f"The weighted sum of these indicators is {weighted_sum:.2f}.\n\n"
        "- Potential Issues Indicated:\n"
        "    The analysis suggests there might be issues related to biased feedback and false accusations. "
        f"{true_indicators} out of {total_indicators} indicators of these issues are present, "
        "indicating a significant likelihood of issues in the evaluated context.\n\n"
        "- Severity Classification of Indicators:\n"
        f"  - Less Severe: {true_indicators_tier_1}\n"
        f"  - Moderately Severe: {true_indicators_tier_2}\n"
        f"  - Most Severe: {true_indicators_tier_3}\n\n"
        "- Conclusion:\n"
        "  - The predominance of moderately to most severe indicators suggests a need for careful scrutiny "
        "and potentially corrective action in the areas where biased feedback or false accusations may occur.\n\n"
    )

    print(summary)

    # Asking to save results to file
    while True:
        save_results = input("Do you want to save the general evaluation results to a file? (yes/no): ").strip().lower()
        if save_results in ['yes', 'y']:
            save_results_to_file(current_time, summary, weighted_percentage, indicators, 'general_evaluation_results')
            sys.exit()
        elif save_results in ['no', 'n']:
            print("Results not saved")
            sys.exit()
        else:
            print("Invalid input, please enter 'yes'(y) or 'no'")


# Indicators for specific cybersecurity evaluation
def evaluate_cybersecurity_indicators(base_tier_weights):
    indicators = {
        "Unsubstantiated accusations of malicious activity\n"
        "(Accusations without concrete proof)": (False, 3, 1.2),

        "Discrepancies in incident reports\n"
        "(Conflicting information in reports of security incidents)":
        (False, 2, 1.1),

        "Inconsistent evidence of unauthorized access\n"
        "(Conflicting evidence or lack thereof for access breaches)":
        (False, 2, 1.0),

        "Claims of data tampering without proof\n"
        "(Allegations of data alteration lacking substantiation)":
        (False, 2, 1.0),

        "Allegations of misuse of privileges\n"
        "(Charges of privilege abuse without corroborating evidence)":
        (False, 3, 1.1),

        "Inconclusive or misinterpreted audit trails\n"
        "(Audit data that is unclear or misread)":
        (False, 1, 0.9),

        "Irregularities in change management records\n"
        "(Anomalies in records, suggesting unreported changes)":
        (False, 1, 0.8),

        "Contradictory witness statements\n"
        "(Conflicting accounts from different individuals)":
        (False, 2, 1.2),

        "Threats of legal action without basis\n"
        "(Unsupported legal threats over alleged actions)":
        (False, 3, 1.3),

        "Variations in network traffic anomalies\n"
        "(Unusual network activity not consistent with typical patterns)":
        (False, 2, 1.0),

        "Lack of corroboration in security logs\n"
        "(Security logs that do not support the allegations made)":
        (False, 2, 1.2),

        "Vague or ambiguous forensic analysis\n"
        "(Forensic findings that are unclear or open to interpretation)":
        (False, 2, 1.0),

        "Inconsistent testimony from team members\n"
        "(Differing accounts of events from team members)": (False, 2, 0.9),

        "Insufficient explanation of tools used\n"
        "(Lack of clarity about the tools used in penetration testing)":
        (False, 1, 0.8),

        "Speculative conclusions in investigation reports\n"
        "(Conclusions based more on guesswork than evidence)": (False, 2, 0.9),

        "Accusations of bypassing protocols without evidence\n"
        "(Charges of ignoring procedures without proof)": (False, 1, 0.7),

        "Timing of security alerts and incidents\n"
        "(Suspicious timing of alerts that may imply ulterior motives)":
        (False, 1, 0.8),

        "Impact of accusations on professional reputation\n"
        "(Allegations that could harm one's professional standing)":
        (False, 3, 1.1),

        "Responses to requests for methodology clarification\n"
        "(Reactions to inquiries about the methods used)": (False, 2, 0.9),

        "Generalizations in accusation without specifics\n"
        "(Broad accusations lacking specific details)": (False, 2, 1.0),

        "Frequency of unsubstantiated claims\n"
        "(Regular occurrence of claims without backing evidence)":
        (False, 1, 0.9),

        "Inconsistency in accusation details\n"
        "(Variances in the details or descriptions of accusations)":
        (False, 2, 1.0),

        "Personal motives in professional accusations\n"
        "(Suspected personal biases influencing professional charges)":
        (False, 2, 1.0),

        "Public disclosure of unverified claims\n"
        "(Sharing unconfirmed allegations publicly)": (False, 1, 0.8),
    }

    # Iterating indicators for answers
    max_length = max(len(indicator) for indicator in indicators.keys())
    print('-' * max_length)
    print("Please answer the following questions"
          "with 'yes'(y) or 'no'(n) or 'exit':\n")
    for indicator in indicators.keys():
        while True:
            response = input(f"{indicator}: ").strip().lower()
            if response in ['yes', 'y']:
                indicators[indicator] = (True, indicators[indicator][1], indicators[indicator][2])
                break
            elif response in ['no', 'n']:
                indicators[indicator] = (False, indicators[indicator][1], indicators[indicator][2])
                break
            elif response == 'exit':
                print("Program exited by user.")
                sys.exit()
            else:
                print("Invalid input. Please answer with 'yes'(y) or 'no'(n) or 'exit'.")
        print("-" * max_length)

    weighted_sum, weighted_percentage = calculate_hybrid_score(indicators, base_tier_weights)
    true_indicators_tier_1 = sum(1 for value, tier, _ in indicators.values()
                                 if value and tier == 1)
    true_indicators_tier_2 = sum(1 for value, tier, _ in indicators.values()
                                 if value and tier == 2)
    true_indicators_tier_3 = sum(1 for value, tier, _ in indicators.values()
                                 if value and tier == 3)
    # Summary
    total_indicators = len(indicators)
    true_indicators = sum(1 for value, _, _ in indicators.values() if value)

    summary = (
        "• Indicator Overview:\n"
        f"• Of {total_indicators} indicators reviewed for potential false accusations against "
        f"cybersecurity and penetration testing personnel, {true_indicators} have been flagged as concerns, "
        f"accounting for {weighted_percentage:.2f}% of the maximum possible score.\n"
        f"The weighted sum of these indicators is {weighted_sum:.2f}.\n"
        "• This indicates a notable level of unjust criticism or unsubstantiated allegations within the "
        "cybersecurity field.\n"
        "• Detailed assessment (classification of severity):\n"
        f"• Minor misunderstandings: {true_indicators_tier_1} indicators suggest minor misunderstandings or "
        "procedural discrepancies. possibly due to technical complexities or rapid changes in cybersecurity practices.\n"
        f"• Moderate allegations: {true_indicators_tier_2} indicators point to moderate issues, "
        "potentially arising from communication gaps, technical misinterpretations, or the specialized nature "
        "of cybersecurity work.\n"
        f"• Severe allegations: {true_indicators_tier_3} indicators relate to severe false accusations or allegations "
        "that could significantly impact professional reputation, team morale, and operational integrity.\n"
        "• Conclusion and Recommendations:\n"
            "• The analysis underscores the need for clear communication, robust and "
        "clear documentation, and fair assessment practices in cybersecurity "
        "environments.\n"
        "• Particular attention must be given to severe false allegations, requiring thorough "
    "investigation to ensure accountability and maintain integrity within the team.\n"
        "• Emphasizing continuous education on the evolving nature of cybersecurity "
        "threats and the importance of a supportive team culture is crucial to "
        "mitigate these issues.\n"
        "• This approach will foster a more trustworthy working "
        "environment for cybersecurity professionals, ensuring team efficiency and "
        "operational effectiveness."
            )

    print(summary)

    # Asking user to print results to file
    while True:
        save_results = input("Do you want to save the cybersecurity evaluation results to a file? (yes/no): ").strip().lower()
        if save_results in ['yes', 'y']:
            save_results_to_file(current_time, summary, weighted_percentage, indicators, 'cybersecurity_evaluation_results')
            sys.exit()
        elif save_results in ['no', 'n']:
            print("Results not saved")
            sys.exit()
        else:
            print("Invalid input, please enter 'yes'(y) or 'no'")


# Function for calculating two values, tier and weights
def calculate_hybrid_score(indicators, base_tier_weights):
    weighted_sum = sum(
        base_tier_weights[tier] * weight_modifier
        for value, tier, weight_modifier in indicators.values() if value
    )
    max_possible_score = sum(
        base_tier_weights[tier] * weight_modifier
        for _, tier, weight_modifier in indicators.values()
    )
    weighted_percentage = (weighted_sum / max_possible_score) * 100
    return weighted_sum, weighted_percentage

# Function for saving results to file
def save_results_to_file(current_time, summary, weighted_percentage, indicators, prefix):
    line = 50 * '-'
    filename = get_next_filename(prefix)
    with open(filename, 'w') as file:
        file.write(f"{current_time}\n\n")
        file.write(f"Summary:\n{summary}\n")
        file.write(f"\nPercentage of True Indicators:{weighted_percentage:.2f}%\n\n")
        for indicator, (value, _, _) in indicators.items():
            file.write(f"{line}\n{indicator}\n: {'Yes' if value else 'No'}\n")
    print(f"Results saved to {filename}")


# Function for not overwriting file when saving new results
def get_next_filename(prefix):
    counter = 0
    while True:
        counter += 1
        filename = f"{prefix}{counter:02}.txt" if counter > 1 else f"{prefix}.txt"
        if not os.path.exists(filename):
            return filename


# Function for textwrapping
def wwrap(text):
    wrapped_text = textwrap.fill(text, width=79)
    return wrapped_text


# This is the main funciton which has the main menu
def main():
    print("""
░▒█▀▀▄░█▀▀▄░█▀▀▄░█▀▀▄░░░░▒█▀▀▀█░█▀▀▄░█░▄░█▀▀▄
░▒█▄▄▀░█▄▄█░█░▒█░█░▒█░▀▀░░▀▀▀▄▄░█▄▄█░█▀▄░█▄▄█
░▒█░▒█░▀░░▀░▀░░▀░▀░░▀░░░░▒█▄▄▄█░▀░░▀░▀░▀░▀░░▀
    """)
    # Define base_tier_weights based on the previous indicators
    base_tier_weights = {
        1: 1,  # For less severe indicators
        2: 2,  # For moderately severe indicators
        3: 3   # For most severe indicators
    }

    print("Choose the type of evaluation:")
    print("1: Cybersecurity Evaluation")
    print("2: General Evaluation")

    while True:
        choice = input("Enter your choice (1 or 2 or 'exit'): ")
        if choice == '1':
            evaluate_cybersecurity_indicators(base_tier_weights)
        elif choice == '2':
            evaluate_general_indicators(base_tier_weights)
        elif choice == 'exit':
            break
        else:
            print("Invalid choice. Please enter '1' or '2' or 'exit'")


if __name__ == "__main__":
    main()
