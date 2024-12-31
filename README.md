# **CONNECT FOUR GAME WITH AI**  
This project is a digital implementation of the classic Connect Four game, enhanced with various gameplay features and AI algorithms to deliver an engaging experience for players of all skill levels.  
 ‎ 
## FEATURES  

### Gameplay Modes  
- Player vs. Player  
- Player vs. AI (with varying difficulty levels)  
- AI vs. AI  

### AI Difficulties  
- **Easy**: Random moves with no strategy.  
- **Intermediate**: Basic heuristics for immediate opportunities or blocking.  
- **Hard**: Minimax algorithm with a depth of 4.  
- **Impossible**: Minimax algorithm with a depth of 6.  
- **Godmode**: Nearly perfect play using a depth of 7.  

### AI Enhancements  
- Minimax with alpha-beta pruning for efficiency.  
- Heuristic evaluation to prioritize winning or blocking opportunities.  

### Evolutionary AI with Genetic Algorithm  
- Evolving strategies to optimize gameplay.  
- Fitness evaluation and strategy refinement across generations.  
‎ 
## **TECHNICAL DETAILS**  

### State Representation  
- A grid of 7 columns and 6 rows, supporting trillions of possible configurations.  

### AI Decision-Making  
- Minimax algorithm explores game states to determine optimal moves, with scoring based on heuristic evaluations.  

### Genetic Algorithm  
- Strategies evolve over 500 generations through crossover and mutation to improve performance against minimax AI.  
‎ 
## **STRUCTURE**  

### Code Organization  
- `variables.py`: Global variables for easy maintenance.  
- `functions.py`: Core game logic.  
- `ui_components.py`: User interface components.  
- `score_ai.py`: Scoring heuristics for AI.  
- `minmax_ai.py`: Minimax algorithm implementation.  
- `genetic.py`: Evolutionary AI logic.  
- `game.py`: Main game loop.  

---

This implementation offers an accessible and challenging digital version of Connect Four, blending AI sophistication with classic gameplay elements.
