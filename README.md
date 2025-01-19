# mastermind-ai

This project is an implementation of an AI player for the game Mastermind. The AI player uses deep reinforcement learning techniques to learn and improve its gameplay strategy.

## Requisitos

- Python 3.8 o superior
- uv (gestor de paquetes moderno para Python)
- Entorno virtual de Python (recomendado)

## Instalación

1. Instala uv si no lo tienes instalado:
```bash
pip install uv
```

2. Clona el repositorio:
```bash
git clone https://github.com/yourusername/mastermind-ai.git
cd mastermind-ai
```

3. Crea y activa un entorno virtual con uv:
```bash
uv venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

4. Instala las dependencias con uv:
```bash
uv pip install -r requirements.txt
```

## Uso

1. Para entrenar el modelo de IA:
```bash
python train_mastermind_ai.py
```

2. Para probar el entorno de Mastermind:
```bash
python test_mastermind_env.py
```

3. Para jugar contra la IA entrenada:
```bash
python play_mastermind.py
```

### Configuración

Puedes modificar los parámetros de entrenamiento y del juego en el archivo `config.py`. Algunos parámetros importantes son:

- `EPISODES`: Número de episodios de entrenamiento
- `LEARNING_RATE`: Tasa de aprendizaje para el modelo
- `BOARD_SIZE`: Tamaño del tablero de Mastermind
- `NUM_COLORS`: Número de colores disponibles en el juego

### Visualización del Entrenamiento

El progreso del entrenamiento se puede visualizar usando TensorBoard:

```bash
tensorboard --logdir=logs
```

Luego, abre tu navegador en `http://localhost:6006` para ver las métricas de entrenamiento.



## References

- <https://neptune.ai/blog/the-best-tools-for-reinforcement-learning-in-python>
- <https://huggingface.co/blog/deep-rl-intro>
- <https://www.analyticsvidhya.com/blog/2019/04/introduction-deep-q-learning-python/>
- <https://huggingface.co/learn/deep-rl-course/unit1/introduction>
- <https://towardsdatascience.com/how-to-teach-an-ai-to-play-games-deep-reinforcement-learning-28f9b920440a>
- <https://github.com/maurock/snake-ga>
- <https://medium.com/@eduardogarrido90/why-deep-reinforcement-learning-is-going-to-be-the-next-big-deal-in-ai-2e796bdf47d2>

## Some Examples

- <https://towardsdatascience.com/reinforcement-learning-with-python-part-1-creating-the-environment-dad6e0237d2d>
- <https://towardsdatascience.com/deep-reinforcement-learning-with-python-part-2-creating-training-the-rl-agent-using-deep-q-d8216e59cf31>
- <https://towardsdatascience.com/deep-reinforcement-learning-with-python-part-3-using-tensorboard-to-analyse-trained-models-606c214c14c7>

## Gym / Tensorforce

- https://github.com/tensorforce/tensorforce
- https://tensorforce.readthedocs.io/en/latest/basics/getting-started.html
- https://gymnasium.farama.org/content/basic_usage/