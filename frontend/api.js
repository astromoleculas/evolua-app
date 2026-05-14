/**
 * API Cliente para EVOLUA
 * Lida com todas as requisições para o backend
 */

class EvoluaAPI {
  constructor(baseURL = "http://localhost:5000") {
    this.baseURL = baseURL;
    this.token = localStorage.getItem("access_token");
  }

  /**
   * Fazer requisição genérica
   */
  async request(endpoint, method = "GET", data = null) {
    const url = `${this.baseURL}${endpoint}`;
    const options = {
      method,
      headers: {
        "Content-Type": "application/json",
      },
    };

    if (this.token) {
      options.headers["Authorization"] = `Bearer ${this.token}`;
    }

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Erro na requisição");
    }

    return await response.json();
  }

  // ==================== AUTENTICAÇÃO ====================

  async register(
    name,
    email,
    password,
    objective = "hipertrofia",
    level = "iniciante",
  ) {
    const result = await this.request("/api/auth/register", "POST", {
      name,
      email,
      password,
      objective,
      level,
    });

    if (result.access_token) {
      this.token = result.access_token;

      localStorage.setItem("access_token", this.token);
      localStorage.setItem("user_id", result.user_id);
    }

    return result;
  }

  async login(email, password) {
    const result = await this.request("/api/auth/login", "POST", {
      email,
      password,
    });

    if (result.access_token) {
      this.token = result.access_token;
      localStorage.setItem("access_token", this.token);
      localStorage.setItem("user_id", result.user_id);
    }

    return result;
  }

  logout() {
    this.token = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
  }

  // ==================== PERFIL ====================

  async getProfile() {
    return await this.request("/api/users/profile", "GET");
  }

  async updateProfile(data) {
    return await this.request("/api/users/profile", "PUT", data);
  }

  // ==================== PLANOS ====================

  async getPlans() {
    return await this.request("/api/plans", "GET");
  }

  async createPlan() {
    return await this.request("/api/plans", "POST", {});
  }

  async getPlanDetails(planId) {
    return await this.request(`/api/plans/${planId}`, "GET");
  }

  // ==================== TREINOS ====================

  async createWorkout(trainingSessionId) {
    return await this.request("/api/workouts", "POST", {
      training_session_id: trainingSessionId,
    });
  }

  async logExercise(
    workoutId,
    exerciseId,
    setsCompleted,
    actualReps,
    weightPerSet,
    difficultyFeedback,
  ) {
    return await this.request(`/api/workouts/${workoutId}/exercise`, "POST", {
      exercise_id: exerciseId,
      sets_completed: setsCompleted,
      actual_reps: actualReps,
      weight_per_set: weightPerSet,
      difficulty_feedback: difficultyFeedback,
    });
  }

  async completeWorkout(workoutId, durationMinutes) {
    return await this.request(`/api/workouts/${workoutId}/complete`, "PUT", {
      duration_minutes: durationMinutes,
    });
  }

  async getUserWorkouts() {
    const userId = localStorage.getItem("user_id");
    return await this.request(`/api/workouts/${userId}`, "GET");
  }

  // ==================== GAMIFICAÇÃO ====================

  async getMedals() {
    const userId = localStorage.getItem("user_id");
    return await this.request(`/api/medals/${userId}`, "GET");
  }

  async getStats() {
    const userId = localStorage.getItem("user_id");
    return await this.request(`/api/stats/${userId}`, "GET");
  }

  // ==================== PROGRESSO ====================

  async logProgress(
    weight,
    bodyMeasurements = {},
    photoUrl = null,
    notes = "",
  ) {
    return await this.request("/api/progress", "POST", {
      weight,
      body_measurements: bodyMeasurements,
      photo_url: photoUrl,
      notes,
    });
  }

  async getProgressHistory() {
    const userId = localStorage.getItem("user_id");
    return await this.request(`/api/progress/${userId}`, "GET");
  }

  async updateProgress(progressId, weight, notes = "") {
    return await this.request(`/api/progress/${progressId}`, "PUT", {
      weight,
      notes,
    });
  }

  // ==================== EXERCÍCIOS ====================

  async getExercises() {
    return await this.request("/api/exercises", "GET");
  }
}

// Criar instância global
const api = new EvoluaAPI();
