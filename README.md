
# Virtual Quiz Game 🌟

The **Virtual Quiz Game** is an interactive platform designed to educate children about potential outer-world threats through engaging quizzes. The game uses CSV files for managing questions and answers, allowing for straightforward customization.

---

## Features

- **Interactive Gameplay**: Players answer multiple-choice questions in a fun and educational format.
- **Educational Focus**: Teaches kids about outer-world threats, promoting awareness and critical thinking.
- **CSV-Based Data**: Easily add, modify, or manage questions using CSV files.
- **Gamified Experience**: Scoring and feedback systems enhance player engagement.

---

## Getting Started

### Prerequisites

To run the Virtual Quiz Game, ensure you have:

- Python 3.7 or higher
- Tkinter (for GUI)
- Pandas (for handling CSV files)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Aniket-a14/Virtual_Quiz_Game.git
   cd Virtual_Quiz_Game
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Play

1. **Launch the Game**:
   Run the main script:
   ```bash
   python main.py
   ```

2. **Select Difficulty**:
   Choose a difficulty level (e.g., Easy, Medium, Hard).

3. **Answer Questions**:
   - Questions are presented as multiple-choice options.
   - Select the correct answer to score points.

4. **View Results**:
   - At the end of the quiz, view your score and feedback.

---

## Project Structure

```
Virtual_Quiz_Game/
│
├── assets/               # Images, audio, and other static assets
├── data/
│   ├── questions_easy.csv      # Easy-level questions
│   ├── questions_medium.csv    # Medium-level questions
│   ├── questions_hard.csv      # Hard-level questions
│
├── src/
│   ├── gui.py            # GUI implementation using Tkinter
│   ├── game_logic.py     # Core quiz logic
│   ├── utils.py          # Utility functions for CSV handling
│
├── main.py               # Entry point for the game
├── requirements.txt      # Dependencies
├── README.md             # Project documentation
```

---

## Customization

### Adding Questions

1. Open the appropriate CSV file from the `data/` folder:
   - `questions_easy.csv`
   - `questions_medium.csv`
   - `questions_hard.csv`

2. Add new rows in the following format:
   ```csv
   Question,Option1,Option2,Option3,Option4,Answer
   What is the nearest planet to the Sun?,Earth,Venus,Mercury,Mars,Mercury
   ```

3. Save the file and relaunch the game to include the new questions.

---

## Future Enhancements

- **Dynamic Question Pool**: Combine questions from multiple CSV files during gameplay.
- **Multiplayer Mode**: Enable competitive play for groups.
- **Timer Functionality**: Add time limits for each question to increase challenge.
- **Mobile Compatibility**: Adapt the game for mobile platforms.

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests for improvements or bug fixes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

Special thanks to contributors and testers for making this project possible. 🌟
