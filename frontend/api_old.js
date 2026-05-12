const API_BASE_URL = "http://localhost:5000/api";

class EvoluaAPI {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "API Error");
    }

    return response.json();
  }

  // User endpoints
  async createUser(userData) {
    return this.request("/users", {
      method: "POST",
      body: JSON.stringify(userData),
    });
  }

  async getUser(userId) {
    return this.request(`/users/${userId}`);
  }

  async updateUser(userId, userData) {
    return this.request(`/users/${userId}`, {
      method: "PUT",
      body: JSON.stringify(userData),
    });
  }

  async loginUser(email) {
    return this.request(`/users/email/${email}`);
  }

  // Exercise endpoints
  async getExercises(filters = {}) {
    let url = "/exercises";
    const params = new URLSearchParams();

    if (filters.muscle_group)
      params.append("muscle_group", filters.muscle_group);
    if (filters.difficulty) params.append("difficulty", filters.difficulty);

    if (params.toString()) {
      url += `?${params.toString()}`;
    }

    return this.request(url);
  }

  async createExercise(exerciseData) {
    return this.request("/exercises", {
      method: "POST",
      body: JSON.stringify(exerciseData),
    });
  }

  // Plan endpoints
  async createPlan(planData) {
    return this.request("/plans", {
      method: "POST",
      body: JSON.stringify(planData),
    });
  }

  async getPlan(planId) {
    return this.request(`/plans/${planId}`);
  }

  async getUserPlans(userId) {
    return this.request(`/plans/user/${userId}`);
  }

  async deletePlan(planId) {
    return this.request(`/plans/${planId}`, {
      method: "DELETE",
    });
  }

  // Workout endpoints
  async createWorkout(workoutData) {
    return this.request("/workouts", {
      method: "POST",
      body: JSON.stringify(workoutData),
    });
  }

  async getUserWorkouts(userId) {
    return this.request(`/workouts/${userId}`);
  }

  // Progress endpoints
  async logProgress(progressData) {
    return this.request("/progress", {
      method: "POST",
      body: JSON.stringify(progressData),
    });
  }

  async getUserProgress(userId) {
    return this.request(`/progress/${userId}`);
  }

  async getGamificationStats(userId) {
    return this.request(`/gamification/stats/${userId}`);
  }

  // Medal endpoints
  async getUserMedals(userId) {
    return this.request(`/medals/${userId}`);
  }

  async awardMedal(medalData) {
    return this.request("/medals", {
      method: "POST",
      body: JSON.stringify(medalData),
    });
  }

  // Health check
  async health() {
    return this.request("/health");
  }
}

// Create global API instance
const api = new EvoluaAPI();
