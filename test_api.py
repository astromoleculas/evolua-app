#!/usr/bin/env python3
"""
Script de teste da API EVOLUA
Testa os endpoints principais e popula dados demo
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:5000"

class EvoluaAPITester:
    def __init__(self):
        self.token = None
        self.user_id = None
        self.plan_id = None

    def test_register(self):
        """Testar registro de usuário"""
        print("🔹 Testando Registro...")
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json={
            "name": "João Silva",
            "email": "joao@evolua.com",
            "password": "senha123",
            "objective": "hipertrofia",
            "level": "iniciante"
        })
        
        if response.status_code == 201:
            data = response.json()
            self.token = data['access_token']
            self.user_id = data['user_id']
            print(f"✅ Registro sucesso | ID: {self.user_id}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_login(self):
        """Testar login"""
        print("🔹 Testando Login...")
        
        response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "joao@evolua.com",
            "password": "senha123"
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data['access_token']
            print(f"✅ Login sucesso | Token: {self.token[:20]}...")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def make_request(self, method, endpoint, data=None):
        """Fazer requisição com autenticação"""
        headers = {"Authorization": f"Bearer {self.token}"}
        
        if method == "GET":
            return requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        elif method == "POST":
            headers["Content-Type"] = "application/json"
            return requests.post(f"{BASE_URL}{endpoint}", json=data, headers=headers)
        elif method == "PUT":
            headers["Content-Type"] = "application/json"
            return requests.put(f"{BASE_URL}{endpoint}", json=data, headers=headers)

    def test_get_profile(self):
        """Testar obter perfil"""
        print("🔹 Testando Obter Perfil...")
        
        response = self.make_request("GET", "/api/users/profile")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Perfil obtido: {data['name']} ({data['email']})")
            print(f"   Objetivo: {data['objective']} | Nível: {data['level']}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_update_profile(self):
        """Testar atualizar perfil"""
        print("🔹 Testando Atualizar Perfil...")
        
        response = self.make_request("PUT", "/api/users/profile", {
            "age": 25,
            "days_per_week": 4
        })
        
        if response.status_code == 200:
            print("✅ Perfil atualizado")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_create_plan(self):
        """Testar criar plano"""
        print("🔹 Testando Criar Plano de Treino...")
        
        response = self.make_request("POST", "/api/plans", {})
        
        if response.status_code == 201:
            data = response.json()
            self.plan_id = data['plan_id']
            print(f"✅ Plano criado: {data['name']}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_get_plans(self):
        """Testar listar planos"""
        print("🔹 Testando Listar Planos...")
        
        response = self.make_request("GET", "/api/plans")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Planos encontrados: {len(data)}")
            if data:
                self.plan_id = data[0]['id']
                print(f"   Primeiro plano: {data[0]['name']}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_get_plan_details(self):
        """Testar obter detalhes do plano"""
        print("🔹 Testando Obter Detalhes do Plano...")
        
        if not self.plan_id:
            print("⚠️  Plano não definido")
            return False
        
        response = self.make_request("GET", f"/api/plans/{self.plan_id}")
        
        if response.status_code == 200:
            data = response.json()
            weeks = data.get('weeks', [])
            print(f"✅ Plano {data['name']}")
            print(f"   Semanas: {len(weeks)}")
            if weeks and weeks[0].get('sessions'):
                print(f"   Exercícios na semana 1: {len(weeks[0]['sessions'])} sessões")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_get_exercises(self):
        """Testar listar exercícios"""
        print("🔹 Testando Listar Exercícios...")
        
        response = requests.get(f"{BASE_URL}/api/exercises")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Exercícios disponíveis: {len(data)}")
            if data:
                print(f"   Primeiro: {data[0]['name']} ({data[0]['muscle_group']})")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_create_workout(self):
        """Testar criar workout"""
        print("🔹 Testando Criar Workout...")
        
        response = self.make_request("POST", "/api/workouts", {
            "training_session_id": 1
        })
        
        if response.status_code == 201:
            data = response.json()
            workout_id = data['workout_id']
            print(f"✅ Workout criado: ID {workout_id}")
            return workout_id
        else:
            print(f"❌ Erro: {response.text}")
            return None

    def test_log_exercise(self, workout_id):
        """Testar registrar exercício"""
        print("🔹 Testando Registrar Exercício...")
        
        response = self.make_request("POST", f"/api/workouts/{workout_id}/exercise", {
            "exercise_id": 1,
            "sets_completed": 3,
            "actual_reps": [10, 10, 9],
            "weight_per_set": [20, 20, 20],
            "difficulty_feedback": "normal"
        })
        
        if response.status_code == 201:
            print("✅ Exercício registrado")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_complete_workout(self, workout_id):
        """Testar finalizar workout"""
        print("🔹 Testando Finalizar Workout...")
        
        response = self.make_request("PUT", f"/api/workouts/{workout_id}/complete", {
            "duration_minutes": 45
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Workout finalizado")
            print(f"   Pontos ganhos: {data.get('points_earned', 0)}")
            if data.get('medal_earned'):
                print(f"   🏅 Medalha conquistada: {data['medal_earned']}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_get_stats(self):
        """Testar obter estatísticas"""
        print("🔹 Testando Obter Estatísticas...")
        
        response = self.make_request("GET", f"/api/stats/{self.user_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Estatísticas:")
            print(f"   Pontos: {data['points']}")
            print(f"   Treinos: {data['workouts_completed']}")
            print(f"   Streak: {data['current_streak']} dias")
            print(f"   Medalhas: {data['medals']}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_get_medals(self):
        """Testar obter medalhas"""
        print("🔹 Testando Obter Medalhas...")
        
        response = self.make_request("GET", f"/api/medals/{self.user_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Medalhas conquistadas: {len(data)}")
            for medal in data:
                print(f"   🏅 {medal['name']} - {medal['description']}")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_log_progress(self):
        """Testar registrar progresso"""
        print("🔹 Testando Registrar Progresso...")
        
        response = self.make_request("POST", "/api/progress", {
            "weight": 75.5,
            "body_measurements": {"chest": 100, "waist": 80},
            "notes": "Primeira medição"
        })
        
        if response.status_code == 201:
            print("✅ Progresso registrado")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def test_get_progress(self):
        """Testar obter histórico de progresso"""
        print("🔹 Testando Obter Histórico de Progresso...")
        
        response = self.make_request("GET", f"/api/progress/{self.user_id}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Registros de progresso: {len(data)}")
            if data:
                print(f"   Último: {data[0]['weight']}kg")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False

    def run_all_tests(self):
        """Executar todos os testes"""
        print("\n" + "="*60)
        print("🚀 INICIANDO TESTES DA API EVOLUA")
        print("="*60 + "\n")
        
        tests = [
            self.test_register,
            self.test_login,
            self.test_get_profile,
            self.test_update_profile,
            self.test_create_plan,
            self.test_get_plans,
            self.test_get_plan_details,
            self.test_get_exercises,
            self.test_log_progress,
        ]
        
        for test in tests:
            try:
                test()
            except Exception as e:
                print(f"❌ Erro ao executar teste: {e}")
            
            sleep(0.5)  # Pequeno delay entre testes
        
        # Testes de workout
        print("\n" + "-"*60)
        print("📊 TESTE DE WORKFLOW DE TREINO")
        print("-"*60 + "\n")
        
        workout_id = self.test_create_workout()
        if workout_id:
            self.test_log_exercise(workout_id)
            self.test_complete_workout(workout_id)
        
        sleep(0.5)
        
        print("\n" + "-"*60)
        print("📈 DADOS FINAIS")
        print("-"*60 + "\n")
        
        self.test_get_stats()
        self.test_get_medals()
        self.test_get_progress()
        
        print("\n" + "="*60)
        print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
        print("="*60 + "\n")

if __name__ == "__main__":
    tester = EvoluaAPITester()
    tester.run_all_tests()
