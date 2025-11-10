"""
Script para popular o banco de dados com exercícios de exemplo
"""

from app import app, db
from models import Exercise

def seed_exercises():
    """Adiciona exercícios de exemplo ao banco de dados"""

    exercises = [
        # Peito
        Exercise(
            name="Supino Reto com Halteres",
            muscle_group="Peito",
            difficulty="Intermediario",
            description="Exercício fundamental para desenvolvimento do peito",
            instructions="1. Deite-se no banco com pés apoiados no chão\n2. Mantenha os halteres ao nível do peito\n3. Pressione os halteres para cima\n4. Abaixe controladamente",
            safety_tips="Mantenha os cotovelos estáveis. Não jogue os halteres. Use peso apropriado.",
            video_url="https://example.com/supino-reto.mp4"
        ),
        Exercise(
            name="Flexão no Banco",
            muscle_group="Peito",
            difficulty="Iniciante",
            description="Variante mais fácil da flexão tradicional",
            instructions="1. Coloque as mãos no banco\n2. Corpo esticado\n3. Desça dobrando os cotovelos\n4. Suba estendendo os braços",
            safety_tips="Mantenha o corpo reto. Controle o movimento.",
            video_url="https://example.com/flexao-banco.mp4"
        ),

        # Costas
        Exercise(
            name="Puxada Frontal",
            muscle_group="Costas",
            difficulty="Intermediario",
            description="Exercício para desenvolvimento das costas",
            instructions="1. Sente-se na máquina\n2. Pegue a barra com as mãos afastadas\n3. Puxe a barra em direção ao peito\n4. Suba controladamente",
            safety_tips="Evite usar movimento de corpo. Mantenha as costas retas.",
            video_url="https://example.com/puxada-frontal.mp4"
        ),
        Exercise(
            name="Remada Inclinada",
            muscle_group="Costas",
            difficulty="Intermediario",
            description="Excelente para estruturar as costas",
            instructions="1. Incline o tronco em 45 graus\n2. Mantenha os joelhos ligeiramente flexionados\n3. Puxe os halteres em direção ao abdômen\n4. Abaixe controladamente",
            safety_tips="Cuidado com a coluna. Não balance o corpo.",
            video_url="https://example.com/remada-inclinada.mp4"
        ),

        # Pernas
        Exercise(
            name="Supino para Pernas",
            muscle_group="Perna",
            difficulty="Iniciante",
            description="Seguro e eficaz para treinar pernas",
            instructions="1. Sente-se na máquina\n2. Coloque os pés na plataforma\n3. Estenda as pernas\n4. Flexione voltando",
            safety_tips="Não estique completamente o joelho. Mantenha o movimento controlado.",
            video_url="https://example.com/supino-pernas.mp4"
        ),
        Exercise(
            name="Agachamento com Peso",
            muscle_group="Perna",
            difficulty="Avancado",
            description="Exercício fundamental para força nas pernas",
            instructions="1. De pé com os pés afastados na largura dos ombros\n2. Barra nos ombros\n3. Abaixe como se fosse sentar\n4. Suba estendendo as pernas",
            safety_tips="Mantenha as costas retas. Joelhos não passem a ponta do pé.",
            video_url="https://example.com/agachamento.mp4"
        ),
        Exercise(
            name="Legpress",
            muscle_group="Perna",
            difficulty="Intermediario",
            description="Máquina excelente para pernas",
            instructions="1. Sente-se na máquina\n2. Coloque os pés na plataforma\n3. Estenda as pernas empurrando\n4. Flexione voltando",
            safety_tips="Não estique completamente o joelho. Respirar é importante.",
            video_url="https://example.com/legpress.mp4"
        ),

        # Braços
        Exercise(
            name="Rosca Direta",
            muscle_group="Braço",
            difficulty="Iniciante",
            description="Exercício fundamental para bíceps",
            instructions="1. De pé com halteres nas mãos\n2. Braços estendidos\n3. Flexione os cotovelos levantando os halteres\n4. Abaixe controladamente",
            safety_tips="Não oscile o corpo. Mantenha os cotovelos próximos ao corpo.",
            video_url="https://example.com/rosca-direta.mp4"
        ),
        Exercise(
            name="Rosca Inversa",
            muscle_group="Braço",
            difficulty="Intermediario",
            description="Exercício para bíceps e antebraço",
            instructions="1. De pé com halteres nas mãos com as palmas viradas para baixo\n2. Braços estendidos\n3. Flexione os cotovelos\n4. Abaixe controladamente",
            safety_tips="Mantenha os cotovelos imóveis. Controle o movimento.",
            video_url="https://example.com/rosca-inversa.mp4"
        ),
        Exercise(
            name="Extensão de Tríceps",
            muscle_group="Braço",
            difficulty="Iniciante",
            description="Isolamento para tríceps",
            instructions="1. De pé com o haltere atrás da cabeça\n2. Estenda os braços para cima\n3. Abaixe trazendo o haltere atrás da cabeça",
            safety_tips="Mantenha os cotovelos apontados para frente. Movimento controlado.",
            video_url="https://example.com/extensao-triceps.mp4"
        ),

        # Ombros
        Exercise(
            name="Desenvolvimento com Halteres",
            muscle_group="Ombro",
            difficulty="Intermediario",
            description="Exercício essencial para desenvolvimento de ombros",
            instructions="1. De pé ou sentado com halteres ao nível dos ombros\n2. Estenda os braços para cima\n3. Abaixe voltando à posição inicial",
            safety_tips="Não arquear a coluna. Movimento controlado.",
            video_url="https://example.com/desenvolvimento.mp4"
        ),
        Exercise(
            name="Elevação Lateral",
            muscle_group="Ombro",
            difficulty="Iniciante",
            description="Isolamento para ombro lateral",
            instructions="1. De pé com halteres nas laterais\n2. Levante os halteres até a altura dos ombros\n3. Abaixe controladamente",
            safety_tips="Cotovelos ligeiramente flexionados. Evite balanço.",
            video_url="https://example.com/elevacao-lateral.mp4"
        ),
    ]

    with app.app_context():
        # Verificar se já existe
        if Exercise.query.first():
            print("Exercícios já existem no banco de dados.")
            return

        for exercise in exercises:
            db.session.add(exercise)

        db.session.commit()
        print(f"✓ {len(exercises)} exercícios adicionados ao banco de dados com sucesso!")

if __name__ == '__main__':
    seed_exercises()
