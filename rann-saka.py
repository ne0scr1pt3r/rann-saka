"""
Project: Rann-Saka
Description: A comprehensive tool for evaluating unfounded allegations in the Cybersecurity domain.
Author: ne0scr1pt3r
GitHub Url: https://github.com/ne0scr1pt3r/rann-saka
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
import random

current_time = time.ctime()

# conditional non-linear weight adjustment
def conditional_weights_non_linear(key_indicator, related_indicators, base_factor, indicators):
    if indicators[key_indicator][0]:
        _, key_tier, key_weight = indicators[key_indicator]
        indicators[key_indicator] = (True, key_tier, key_weight * (base_factor ** key_tier))
        for ind in related_indicators:
            value, tier, weight = indicators[ind]
            indicators[ind] = (value, tier, weight * (base_factor ** tier))
    else:
        for ind in related_indicators:
            value, tier, weight = indicators[ind]
            if value:
                indicators[ind] = (value, tier, weight * ((base_factor - 0.25) ** tier))


# function randomness for unpredictibility
def apply_randomness(indicators):
    for _, cat_indicators in indicators.items():
        for indicator, (value, tier, weight) in cat_indicators.items():
            random_factor = random.uniform(0.9, 1.1)
            new_weight = weight * random_factor
            cat_indicators[indicator] = (value, tier, new_weight)


# Indicators for general evaluation
def evaluate_general_indicators(base_tier_weights):
    indicators = {
        # Feedback and communication
        'Feedback and communication': {
            "Consistent negative feedback\n(Frequent negative feedback, "
            "regardless of performance or improvement)": (False, 3, 1.3),
            "Vague or non-specific criticism\n(Criticism that lacks clear and "
            "actionable points)": (False, 2, 1.0),
            "Personal rather than professional feedback\n(Feedback focuses on "
            "personal traits rather than professional skills)": (False, 2, 1.0),
            "Contradictory information\n(Receiving conflicting instructions or "
            "feedback)": (False, 3, 1.1),
            "Inconsistency over time\n(Feedback or expectations that change "
            "unpredictably over time)": (False, 2, 1.0),
            "Contradiction with documented facts\n(Feedback or claims that "
            "contradict documented evidence)": (False, 3, 1.2),
            "Discrepancy with colleague feedback\n(Significant differences "
            "between feedback from different colleagues)": (False, 2, 0.9),
            "Unwillingness to provide details\n(Reluctance to give detailed "
            "information or clarification)": (False, 1, 0.8),
            "Feedback based on rumor or speculation\n(Feedback that is not "
            "based on direct observation or evidence)": (False, 2, 0.9),
            "Unconstructive feedback\n(Feedback that doesn't offer a clear path "
            "to improvement)": (False, 2, 1.0),
            "Frequent criticism\n(Regular and persistent criticism)": (False, 1, 0.9),
            "Inconsistency\n(Lack of consistency in feedback or expectations)": (False, 2, 1.0),
            "Personal, not professional\n(Focus on personal attributes rather "
            "than professional performance)": (False, 2, 1.0),
            "Public criticism\n(Criticism delivered in a public setting)": (False, 1, 0.8),
            "No recognition of improvement\n(Ignoring or not acknowledging "
            "improvements made)": (False, 2, 0.9),
            "Feedback contrary to previous evaluations\n(Feedback that "
            "contradicts earlier evaluations)": (False, 3, 1.2)
        },
        # career impact and professionalism
        'Career impact and professionalism': {
            "Decline in job offers\n(Noticeable decrease in job offers or "
            "opportunities)": (False, 3, 1.4),
            "Impact on career opportunities\n(Feedback that adversely affects "
            "future career prospects)": (False, 3, 1.1),
            "Isolation from collaborative opportunities\n(Exclusion from "
            "opportunities for teamwork and collaboration)": (False, 1, 0.8),
            "Exclusion from professional development\n(Being left out of "
            "professional growth and development opportunities)": (False, 1, 0.7),
            "Impact on morale\n(Feedback that negatively affects morale)": (False, 2, 0.9),
            "Negative feedback on areas outside of their oversight\n(Criticism "
            "about aspects outside the employee's control or responsibility)": (False, 1, 0.7),
            "Timing of the accusations or feedback\n(Feedback timing that may "
            "have ulterior motives or context)": (False, 1, 0.8)
        },
        # authenticity and credibility
        'Authenticity and credibility': {
            "Lack of credibility\n(Feedback or instructions lack grounding in "
            "facts or reality)": (False, 3, 1.3),
            "Unverifiable or exaggerated claims\n(Claims or accusations that "
            "cannot be substantiated)": (False, 2, 1.0),
            "Lack of objective evidence\n(Feedback not supported by objective "
            "facts or data)": (False, 2, 1.0),
            "Unusual communication from prospective employers\n(Unexpected or "
            "unconventional communication styles from potential employers)": (False, 1, 0.9),
            "Legal action threats\n(Threats of legal action in response to "
            "actions or performance)": (False, 3, 1.3),
            "Direct warnings\n(Explicit warnings about performance or behavior)": (False, 3, 1.2),
            "Excessive focus on minor errors\n(Overemphasis on small mistakes)": (False, 2, 0.9),
            "Ignoring context\n(Overlooking the context or circumstances of "
            "actions or performance)": (False, 2, 0.9)
        },

        # Management and Support
        'Management and Support': {
            "Lack of support\n(Insufficient support or resources for the role)": (False, 1, 1.0),
            "Comparisons with others\n(Unfavorable comparisons with other "
            "colleagues)": (False, 1, 0.7)
        }
    }

    # Iterating general indicators for answers
    max_length = max(len(indicator) for category in indicators.values() for indicator in category)
    print('-' * max_length)
    print("Please answer the following questions "
          "with 'yes'(y) or 'no'(n) or 'exit':\n")
    for category, cat_indicators in indicators.items():
        print(f"Category: {category}")
        for indicator, (_, tier, weight) in cat_indicators.items():
            while True:
                response = input(f"{indicator}: ").strip().lower()
                if response in ['yes', 'y']:
                    cat_indicators[indicator] = (True, tier, weight)
                    break
                elif response in ['no', 'n']:
                    cat_indicators[indicator] = (False, tier, weight)
                    break
                elif response == 'exit':
                    print("Program exited by user.")
                    sys.exit()
                else:
                    print("Invalid input. Please answer with 'yes'(y) or 'no'(n) or 'exit'.")
            print("-" * max_length)
        key_indicator = next(iter(cat_indicators))
        related_indicators = list(cat_indicators.keys())[1:]

        conditional_weights_non_linear(key_indicator, related_indicators, 1.5, cat_indicators)

    weighted_sum, weighted_percentage = calculate_hybrid_score(indicators, base_tier_weights)
    true_indicators_tier_1 = sum(1 for category in indicators.values() for _, tier, _ in category.values() if tier == 1)
    true_indicators_tier_2 = sum(1 for category in indicators.values() for _, tier, _ in category.values() if tier == 2)
    true_indicators_tier_3 = sum(1 for category in indicators.values() for _, tier, _ in category.values() if tier == 3)
    # Summary
    total_indicators = sum(len(cat_indicators) for cat_indicators in indicators.values())
    true_indicators = sum(1 for category in indicators.values() for value, _, _ in category.values() if value)

    summary = (
        "- Analysis:\n"
        f"    Out of a total of {total_indicators} indicators analyzed, {true_indicators} "
        f"(or {weighted_percentage:.2f}% of the maximum possible score) were identified as true. "
        f"The weighted sum of these indicators is {weighted_sum:.2f}.\n\n"
        "- Potential issues:\n"
        "    The analysis suggests there might be issues related to biased feedback and false accusations. "
        f"{true_indicators} out of {total_indicators} indicators of these issues are present, "
        "indicating a significant likelihood of issues in the evaluated context.\n\n"
        "- Severity classification:\n"
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
        # authorization and access control
        'Authorization and access control': {
            "Unsubstantiated accusations of malicious activity\n"
            "(Accusations without concrete proof)": (False, 3, 1.3),
            "Inconsistent evidence of unauthorized access\n"
            "(Conflicting evidence or lack thereof for access breaches)":
            (False, 2, 1.0),
            "Claims of data tampering without proof\n"
            "(Allegations of data alteration lacking substantiation)":
            (False, 2, 1.0),
            "Allegations of unauthorized network monitoring\n"
            "(claims of unauthorized surveillance or network monitoring without "
            "proof)": (False, 2, 1.0),
            "Claims of inappropriate data access\n"
            "(allegations of accessing sensitive data without permission, lacking "
            "verification)": (False, 2, 1.0),
            "Allegations of misuse of privileges\n"
            "(Charges of privilege abuse without corroborating evidence)":
            (False, 3, 1.1),
            "Accusations of bypassing protocols without evidence\n"
            "(Charges of ignoring procedures without proof)": (False, 1, 0.7),
            "Unverified reports of security protocol violations\n"
            "(claims of security procedures being violated without substantial "
            "evidence)": (False, 3, 1.2),
            "Misinterpreted penetration testing actions\n"
            "(legitimate penetration testing activities perceived as malicious "
            "acts)": (False, 3, 1.1),
            "Insufficient explanation of tools used\n"
            "(Lack of clarity about the tools used in penetration testing)":
            (False, 1, 0.8),
        },
        # reporting and documentation
        'Reporting and documentation': {
            "Discrepancies in incident reports\n"
            "(Conflicting information in reports of security incidents)":
            (False, 2, 1.1),
            "Lack of corroboration in security logs\n"
            "(Security logs that do not support the allegations made)":
            (False, 2, 1.2),
            "Vague or ambiguous forensic analysis\n"
            "(Forensic findings that are unclear or open to interpretation)":
            (False, 2, 1.0),
            "Speculative conclusions in investigation reports\n"
            "(Conclusions based more on guesswork than evidence)": (False, 2, 0.9),
            "Incorrect attribution of malware introduction\n"
            "(blaming personnel for introducing malware without evidence)":
            (False, 3, 1.1),
            "Inconclusive or misinterpreted audit trails\n"
            "(Audit data that is unclear or misread)":
            (False, 1, 0.9),
        },
        # conduct and misunderstandings
        'Conduct and misunderstandings': {
            "Misconstrued intentions in security testing\n"
            "(misinterpretation of security testing procedures as harmful "
            "intentions)": (False, 2, 1.2),
            "Unsatisfactory responses to methodology clarification requests\n"
            "(Responses to inquiries about methods used are inadequate or \n"
            "evasive, potentially leading to misunderstandings or "
            "false accusations)": (False, 2, 0.9),
            "Generalizations in accusation without specifics\n"
            "(Broad accusations lacking specific details)": (False, 2, 1.0),
            "Public disclosure of unverified claims\n"
            "(Sharing unconfirmed allegations publicly)": (False, 1, 0.8),
            "Threats of legal action without basis\n"
            "(Unsupported legal threats over alleged actions)":
            (False, 3, 1.3),
        },
        # team dynamics and communication
        'Team dynamics and communication': {
            "Impact of accusations on professional reputation\n"
            "(Allegations that could harm one's professional standing)":
            (False, 3, 1.3),
            "Contradictory witness statements\n"
            "(Conflicting accounts from different individuals)":
            (False, 2, 1.2),
            "Inconsistent testimony from team members\n"
            "(Differing accounts of events from team members)": (False, 2, 0.9),
            "Personal motives in professional accusations\n"
            "(Suspected personal biases influencing professional charges)":
            (False, 2, 1.0),
            "Inconsistency in accusation details\n"
            "(Variances in the details or descriptions of accusations)":
            (False, 2, 1.0),
            "Mistaken identity in cyber attack attribution\n"
            "(incorrectly identifying individuals as responsible for cyber "
            "attacks)": (False, 2, 1.2),
            "Frequency of unsubstantiated claims\n"
            "(Regular occurrence of claims without backing evidence)":
            (False, 1, 0.9),
            "Timing of security alerts and incidents\n"
            "(Suspicious timing of alerts that may imply ulterior motives)":
            (False, 2, 1.2),
            "Accusations of neglecting security warnings\n"
            "(charges of ignoring important security warnings without factual "
            "basis)": (False, 2, 1.0),
            "Assumed complicity in security breaches\n"
            "(wrongful assumptions of involvement in security breaches)":
            (False, 3, 1.3),
            "Unfounded blame for data leaks\n"
            "(baseless accusations of causing or contributing to data leaks)":
            (False, 2, 1.2),
        }
    }

    # Iterating indicators for answers
    max_length = max(len(indicator) for category in indicators.values() for indicator in category)
    print('-' * max_length)
    print("Please answer the following questions "
          "with 'yes'(y) or 'no'(n) or 'exit':\n")
    for category, cat_indicators in indicators.items():
        print(f"Category: {category}")
        for indicator, (_, tier, weight) in cat_indicators.items():
            while True:
                response = input(f"{indicator}: ").strip().lower()
                if response in ['yes', 'y']:
                    cat_indicators[indicator] = (True, tier, weight)
                    break
                elif response in ['no', 'n']:
                    cat_indicators[indicator] = (False, tier, weight)
                    break
                elif response == 'exit':
                    print("Program exited by user.")
                    sys.exit()
                else:
                    print("Invalid input. Please answer with 'yes'(y) or 'no'(n) or 'exit'.")
            print("-" * max_length)
        key_indicator = next(iter(cat_indicators))
        related_indicators = list(cat_indicators.keys())[1:]

        conditional_weights_non_linear(key_indicator, related_indicators, 1.5, cat_indicators)

    weighted_sum, weighted_percentage = calculate_hybrid_score(indicators, base_tier_weights)
    true_indicators_tier_1 = sum(1 for category in indicators.values() for _, tier, _ in category.values() if tier == 1)
    true_indicators_tier_2 = sum(1 for category in indicators.values() for _, tier, _ in category.values() if tier == 2)
    true_indicators_tier_3 = sum(1 for category in indicators.values() for _, tier, _ in category.values() if tier == 3)

    # Summary
    total_indicators = sum(len(cat_indicators) for cat_indicators in indicators.values())
    true_indicators = sum(1 for category in indicators.values() for value, _, _ in category.values() if value)

    summary = (
        "• Overview:\n"
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
        for category in indicators.values()
        for _, tier, weight_modifier in category.values() if _
    )
    max_possible_score = sum(
        base_tier_weights[tier] * weight_modifier
        for category in indicators.values()
        for _, tier, weight_modifier in category.values()
    )
    weighted_percentage = (weighted_sum / max_possible_score) * 100
    return weighted_sum, weighted_percentage

# Function for saving results to file
def save_results_to_file(current_time, summary, weighted_percentage, indicators, prefix):
    line = 50 * '-'
    filename = get_next_filename(prefix)

    minor_indicators = []
    moderate_indicators = []
    most_severe_indicators = []

    # Iterate through each category and its indicators
    for category, cat_indicators in indicators.items():
        for indicator, (value, tier, _) in cat_indicators.items():
            if value and tier == 1:
                minor_indicators.append(f"{category} - {indicator}")
            elif value and tier == 2:
                moderate_indicators.append(f"{category} - {indicator}")
            elif value and tier == 3:
                most_severe_indicators.append(f"{category} - {indicator}")

    with open(filename, 'w') as file:
        file.write(f"{current_time}\n\n")
        file.write(f"-- Summary --\n{summary}\n\n")
        file.write(f"-- Percentage score -- {weighted_percentage:.2f}%\n\n")
        file.write("-- Severity classification of indicators --\n\n")
        file.write("- Less severe indicators -\n")
        for indicator in minor_indicators:
            file.write(f"{indicator}\n")
        file.write(f"{line}\n\n- Moderately severe indicators -\n")
        for indicator in moderate_indicators:
            file.write(f"{indicator}\n")
        file.write(f"{line}\n\n- Most severe indicators -\n")
        for indicator in most_severe_indicators:
            file.write(f"{indicator}\n")
        file.write("\n\n-- All indicators with all the answers --\n")
        for category, cat_indicators in indicators.items():
            for indicator, (value, _, _) in cat_indicators.items():
                file.write(f"{line}\n{category} - {indicator}\n: {'Yes' if value else 'No'}\n")

    print(f"Results saved to {filename}")


# Function for not overwriting file when saving new results
def get_next_filename(prefix):
    counter = 0
    while True:
        counter += 1
        filename = f"{prefix}{counter:02}.txt" if counter > 1 else f"{prefix}.txt"
        if not os.path.exists(filename):
            return filename


# Textwrapping
def wwrap(text):
    wrapped_text = textwrap.fill(text, width=79)
    return wrapped_text


# This is the main function which has the main menu
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
    print("1: General Evaluation")
    print("2: Cybersecurity Evaluation")

    while True:
        choice = input("Enter your choice (1 or 2 or 'exit'): ")
        if choice == '1':
            evaluate_general_indicators(base_tier_weights)
        elif choice == '2':
            evaluate_cybersecurity_indicators(base_tier_weights)
        elif choice == 'exit':
            break
        else:
            print("Invalid choice. Please enter '1' or '2' or 'exit'")


if __name__ == "__main__":
    main()
