# JD-Design-Project2

Design Project 2 for ECE 1895 - Junior Design

---

## Final Idea
**Breaking Bad Themed**

---

## Description
This game is based on the sequence **Call → Mix → Pay**, inspired by *Breaking Bad*. In the show, a deal often starts with a phone call (**Call**), then the product is made or prepared (**Mix**), and finally payment is exchanged (**Pay**).

The game transforms these three steps into quick physical actions that the player must perform when the system issues a command.

---

## Functional Overview

- The unit includes a **power switch** and a **start button**.
- When powered on, users press the start button to initiate the game.
- Once started, one of three distinct audible commands will be played:
  - “Call It”
  - “Mix It”
  - “Pay It”
- The user must perform one of three corresponding actions within an allocated time window to win the round.
- The internal hardware evaluates whether the input matches the command within the allowed time.

### Scoring & Feedback

- **Correct response:**
  - Earns 1 point
  - Triggers a visual success cue (green LED)

- **Incorrect or late response:**
  - Triggers a “Game Over” sound
  - Activates a red LED to indicate elimination

- After each successful round:
  - Commands continue at progressively shorter time intervals (increasing difficulty)

- The game ends when:
  - The player reaches the maximum score of **99 points**

---

## Team Members

- Wunmi Salami  
- Sydney Dinardo  
- Alex Brunco  
- Deni Ephraim  
