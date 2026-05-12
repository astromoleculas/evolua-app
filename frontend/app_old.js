// Global state
let appState = {
  currentUser: null,
  userId: localStorage.getItem("userId") || null,
};

// Usuários salvos para teste rápido
const SAVED_USERS = [
  {
    name: "Carlos Mendes",
    email: "carlos@example.com",
    password: "senha123",
    objective: "ganho_massa",
    level: "iniciante",
    days: 3,
  },
  {
    name: "Juliana Lima",
    email: "juliana@example.com",
    password: "senha456",
    objective: "perda_peso",
    level: "intermediario",
    days: 4,
  },
  {
    name: "João Silva",
    email: "joao@example.com",
    password: "senha789",
    objective: "tonificacao",
    level: "intermediario",
    days: 5,
  },
];

// DOM Elements
const app = document.getElementById("app");
const pages = document.querySelectorAll(".page");
const navLinks = document.querySelectorAll(".nav-link");

// Initialize app
document.addEventListener("DOMContentLoaded", () => {
  initializeApp();
  setupEventListeners();
});

function initializeApp() {
  if (!appState.userId) {
    showAuthModal();
  } else {
    loadUserData();
    showDashboard();
  }
}

function setupEventListeners() {
  // Navigation
  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const page = link.getAttribute("data-page");
      navigateTo(page);
    });
  });

  // Logout button
  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", handleLogout);
  }

  // Auth form
  const authForm = document.getElementById("auth-form");
  if (authForm) {
    authForm.addEventListener("submit", handleAuth);
  }

  // Usuários salvos
  const newUserBtn = document.getElementById("new-user-btn");
  if (newUserBtn) {
    newUserBtn.addEventListener("click", () => switchAuthTab("new-user"));
  }

  const backBtn = document.getElementById("back-btn");
  if (backBtn) {
    backBtn.addEventListener("click", (e) => {
      e.preventDefault();
      switchAuthTab("saved-users");
    });
  }

  // Renderizar usuários salvos
  renderSavedUsers();

  // Profile form
  const profileForm = document.getElementById("profile-form");
  if (profileForm) {
    profileForm.addEventListener("submit", handleProfileUpdate);
  }

  // Workout form
  const workoutForm = document.getElementById("workout-form");
  if (workoutForm) {
    workoutForm.addEventListener("submit", handleWorkoutSubmit);
  }

  // Progress form
  const progressForm = document.getElementById("progress-form");
  if (progressForm) {
    progressForm.addEventListener("submit", handleProgressSubmit);
  }

  // Buttons
  const startBtn = document.getElementById("start-btn");
  if (startBtn) {
    startBtn.addEventListener("click", () => navigateTo("plans"));
  }

  const createPlanBtn = document.getElementById("create-plan-btn");
  if (createPlanBtn) {
    createPlanBtn.addEventListener("click", () => handleCreatePlan());
  }

  const logWorkoutBtn = document.getElementById("log-workout-btn");
  if (logWorkoutBtn) {
    logWorkoutBtn.addEventListener("click", () => openModal("workout-modal"));
  }

  const logProgressBtn = document.getElementById("log-progress-btn");
  if (logProgressBtn) {
    logProgressBtn.addEventListener("click", () => openModal("progress-modal"));
  }

  // Modal close buttons
  document.querySelectorAll(".close").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const modal = e.target.closest(".modal");
      closeModal(modal);
    });
  });

  // Close modal on outside click
  document.querySelectorAll(".modal").forEach((modal) => {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        closeModal(modal);
      }
    });
  });
}

// Navigation
function navigateTo(pageName) {
  // Hide all pages
  pages.forEach((page) => page.classList.remove("active"));

  // Remove active from nav links
  navLinks.forEach((link) => link.classList.remove("active"));

  // Show selected page
  const page = document.getElementById(`${pageName}-page`);
  if (page) {
    page.classList.add("active");
  }

  // Update nav link
  const link = document.querySelector(`[data-page="${pageName}"]`);
  if (link) {
    link.classList.add("active");
  }

  // Load page data
  if (pageName === "dashboard") {
    loadDashboardData();
  } else if (pageName === "profile") {
    loadProfileData();
  } else if (pageName === "plans") {
    loadPlansData();
  } else if (pageName === "workouts") {
    loadWorkoutsData();
  } else if (pageName === "progress") {
    loadProgressData();
  }
}

function showDashboard() {
  navigateTo("dashboard");
}

// Auth
async function handleAuth(e) {
  e.preventDefault();

  const name = document.getElementById("auth-name").value;
  const email = document.getElementById("auth-email").value;
  const password = document.getElementById("auth-password").value;

  try {
    const user = await api.createUser({
      name,
      email,
      password,
    });

    appState.currentUser = user;
    appState.userId = user.id;

    localStorage.setItem("userId", user.id);
    localStorage.setItem("userName", user.name);

    document.getElementById("auth-name").value = "";
    document.getElementById("auth-email").value = "";
    document.getElementById("auth-password").value = "";

    closeModal(document.getElementById("auth-modal"));
    updateUserName();
    loadUserData();
    showDashboard();
  } catch (error) {
    alert("Erro ao fazer login/registrar: " + error.message);
  }
}

function handleLogout() {
  if (confirm("Tem certeza que deseja sair?")) {
    logout();
  }
}

function logout() {
  // Limpar estado
  appState.currentUser = null;
  appState.userId = null;

  // Limpar localStorage
  localStorage.removeItem("userId");
  localStorage.removeItem("userName");

  // Mostrar modal de login
  showAuthModal();
}

// Load user data
async function loadUserData() {
    if (!appState.userId) {
        console.warn('Nenhum userId definido');
        return;
    }

    try {
        console.log('📊 Carregando dados do usuário:', appState.userId);

        // Carregar gamificação PRIMEIRO
        const stats = await loadGamificationStats(appState.userId);

        // Depois atualizar streak com os dados retornados
        if (stats && stats.streak !== undefined) {
            const streakEl = document.getElementById('streak');
            if (streakEl) streakEl.textContent = stats.streak + ' dias';
        }

        // Carregar gráficos (se existir função)
        if (typeof updateAllCharts === 'function') {
            await updateAllCharts(appState.userId);
        }
    } catch (error) {
        console.error('❌ Erro ao carregar dados:', error);
    }
}

function updateWelcomeMessage() {
  const welcomeMsg = document.getElementById("welcome-message");
  if (welcomeMsg && appState.currentUser) {
    welcomeMsg.textContent = `Bem-vindo, ${appState.currentUser.name}! Vamos continuar sua transformação!`;
  }
}

function updateUserName() {
  const userNameElement = document.getElementById("user-name");
  if (userNameElement && appState.currentUser) {
    userNameElement.textContent = appState.currentUser.name;
  }
}

// Profile
async function loadProfileData() {
  if (!appState.currentUser) {
    return;
  }

  const user = appState.currentUser;

  document.getElementById("name").value = user.name || "";
  document.getElementById("email").value = user.email || "";
  document.getElementById("age").value = user.age || "";
  document.getElementById("objective").value = user.objective || "";
  document.getElementById("level").value = user.level || "";
  document.getElementById("days-per-week").value = user.days_per_week || "";
  document.getElementById("location").value = user.training_location || "";
}

async function handleProfileUpdate(e) {
  e.preventDefault();

  const userData = {
    name: document.getElementById("name").value,
    age: parseInt(document.getElementById("age").value) || null,
    objective: document.getElementById("objective").value,
    level: document.getElementById("level").value,
    days_per_week: parseInt(document.getElementById("days-per-week").value),
    training_location: document.getElementById("location").value,
  };

  try {
    await api.updateUser(appState.userId, userData);
    await loadUserData();
    alert("Perfil atualizado com sucesso!");
  } catch (error) {
    alert("Erro ao atualizar perfil: " + error.message);
  }
}

// Dashboard
async function loadDashboardData() {
  try {
    if (!appState.currentUser) {
      return;
    }

    // Update stats
    document.getElementById("points").textContent =
      appState.currentUser.points || 0;

    // Load recent workouts
    const workouts = await api.getUserWorkouts(appState.userId);
    const recentList = document.getElementById("recent-workouts");

    if (workouts.length === 0) {
      recentList.innerHTML = "<p>Nenhum treino registrado</p>";
    } else {
      recentList.innerHTML = workouts
        .slice(0, 5)
        .map(
          (w) => `
                <div class="workout-item">
                    <div class="workout-info">
                        <h4>${new Date(w.date).toLocaleDateString("pt-BR")}</h4>
                        <p>Duração: ${w.duration_minutes} min | Peso: ${
            w.total_weight || "N/A"
          } kg</p>
                    </div>
                    <span class="badge badge-success">Completo</span>
                </div>
            `
        )
        .join("");
    }

    // Update workouts count
    document.getElementById("workouts-count").textContent = workouts.length;

    // Load medals
    const medals = await api.getUserMedals(appState.userId);
    document.getElementById("medals-count").textContent = medals.length;

    // Calculate streak
    const streak = calculateStreak(workouts);
    document.getElementById("streak").textContent = streak + " dias";
  } catch (error) {
    console.error("Error loading dashboard:", error);
  }
}

/**
 * Calcula o número de dias consecutivos de treino
 */
function calculateStreak(workouts) {
  if (workouts.length === 0) {
    return 0;
  }

  // Ordenar treinos por data (mais recentes primeiro)
  const sortedWorkouts = workouts.sort((a, b) => {
    return new Date(b.date) - new Date(a.date);
  });

  // Converter datas para apenas a data (sem hora)
  // Usar apenas a parte YYYY-MM-DD da string ISO
  const uniqueDates = [];
  const dateSet = new Set();

  sortedWorkouts.forEach((workout) => {
    const date = new Date(workout.date);
    // Extrair apenas YYYY-MM-DD usando o método ISO (UTC)
    const dateKey = date.toISOString().split("T")[0];

    if (!dateSet.has(dateKey)) {
      dateSet.add(dateKey);
      uniqueDates.push(dateKey); // Armazenar como string
    }
  });

  // Se não há treinos, streak é 0
  if (uniqueDates.length === 0) {
    return 0;
  }

  console.log("Datas únicas:", uniqueDates);

  // Converter strings de data para objetos Date em UTC
  const dateDates = uniqueDates.map((dateStr) => {
    const [year, month, day] = dateStr.split("-");
    return new Date(year, parseInt(month) - 1, day);
  });

  let streak = 1; // Pelo menos 1 dia

  // Pegar hoje em UTC
  const today = new Date();
  const todayKey = today.toISOString().split("T")[0];
  const todayDate = new Date(
    todayKey.split("-")[0],
    parseInt(todayKey.split("-")[1]) - 1,
    parseInt(todayKey.split("-")[2])
  );

  console.log("Hoje:", todayKey);
  console.log("Treino mais recente:", uniqueDates[0]);

  // Verificar se o treino mais recente foi hoje ou ontem
  const mostRecentDate = dateDates[0];
  const dayDifference = Math.floor(
    (todayDate - mostRecentDate) / (1000 * 60 * 60 * 24)
  );

  console.log("Diferença de dias:", dayDifference);

  // Se o treino mais recente foi há 2 ou mais dias, streak é 0
  if (dayDifference > 1) {
    console.log("Treino muito antigo, streak zerado");
    return 0;
  }

  // Contar dias consecutivos para trás
  for (let i = 0; i < dateDates.length - 1; i++) {
    const currentDate = dateDates[i];
    const nextDate = dateDates[i + 1];

    // Calcular diferença em dias
    const daysDiff = Math.round(
      (currentDate - nextDate) / (1000 * 60 * 60 * 24)
    );

    console.log(
      `Comparando ${uniqueDates[i]} e ${
        uniqueDates[i + 1]
      }: diferença = ${daysDiff} dias`
    );

    // Se a diferença é exatamente 1 dia, continua o streak
    if (daysDiff === 1) {
      streak++;
    } else {
      // Se não é 1 dia de diferença, para de contar
      break;
    }
  }

  console.log("Streak final:", streak);
  return streak;
}

// Plans
async function loadPlansData() {
  const plansList = document.getElementById("plans-list");
  plansList.innerHTML = "<p>Carregando planos...</p>";

  try {
    const plans = await api.getUserPlans(appState.userId);

    if (plans.length === 0) {
      plansList.innerHTML =
        '<p>Nenhum plano criado. Clique em "Criar Novo Plano" para começar!</p>';
    } else {
      plansList.innerHTML = plans
        .map(
          (p) => `
                <div class="plan-item">
                    <div class="plan-info">
                        <h4>${p.name}</h4>
                        <p>${p.description}</p>
                        <p style="font-size: 0.85rem; color: #6b7280; margin-top: 0.5rem;">
                            📅 ${p.duration_weeks} semanas | 📋 ${
            p.weeks_count
          } semanas planejadas
                        </p>
                        <p style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.25rem;">
                            Criado em ${new Date(
                              p.created_at
                            ).toLocaleDateString("pt-BR")}
                        </p>
                    </div>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="btn btn-secondary" onclick="viewPlanDetails(${
                          p.id
                        })">Ver Detalhes</button>
                        <button class="btn btn-danger" onclick="deletePlanConfirm(${
                          p.id
                        }, '${p.name}')">Deletar</button>
                    </div>
                </div>
            `
        )
        .join("");
    }
  } catch (error) {
    console.error("Error loading plans:", error);
    plansList.innerHTML = "<p>Erro ao carregar planos</p>";
  }
}

async function viewPlanDetails(planId) {
  try {
    const plan = await api.getPlan(planId);
    console.log("Detalhes do plano:", plan);
    alert(
      `Plano: ${plan.name}\n\nSemanas: ${plan.weeks.length}\nExercícios estruturados por semana`
    );
  } catch (error) {
    alert("Erro ao carregar detalhes: " + error.message);
  }
}

function deletePlanConfirm(planId, planName) {
  if (
    confirm(
      `Tem certeza que deseja deletar o plano "${planName}"? Esta ação não pode ser desfeita.`
    )
  ) {
    deletePlan(planId);
  }
}

async function deletePlan(planId) {
  try {
    await api.deletePlan(planId);
    alert("Plano deletado com sucesso!");
    loadPlansData();
  } catch (error) {
    alert("Erro ao deletar plano: " + error.message);
  }
}

async function handleCreatePlan() {
  try {
    const plan = await api.createPlan({
      user_id: appState.userId,
    });

    alert("Plano criado com sucesso!");
    loadPlansData();
  } catch (error) {
    alert("Erro ao criar plano: " + error.message);
  }
}

// Workouts
async function loadWorkoutsData() {
  try {
    const workouts = await api.getUserWorkouts(appState.userId);
    const workoutsList = document.getElementById("workouts-list");

    if (workouts.length === 0) {
      workoutsList.innerHTML = "<p>Nenhum treino registrado</p>";
    } else {
      workoutsList.innerHTML = workouts
        .map(
          (w) => `
                <div class="workout-item">
                    <div class="workout-info">
                        <h4>${new Date(w.date).toLocaleDateString("pt-BR", {
                          weekday: "long",
                          year: "numeric",
                          month: "long",
                          day: "numeric",
                        })}</h4>
                        <p>Duração: ${w.duration_minutes} min | Peso total: ${
            w.total_weight || "N/A"
          } kg</p>
                        <p>Calorias: ${w.calories_burned || 0} kcal</p>
                    </div>
                    <span class="badge badge-success">Completo</span>
                </div>
            `
        )
        .join("");
    }
  } catch (error) {
    console.error("Error loading workouts:", error);
  }
}

async function handleWorkoutSubmit(e) {
  e.preventDefault();

  const workoutData = {
    user_id: appState.userId,
    duration_minutes: parseInt(
      document.getElementById("workout-duration").value
    ),
    total_weight:
      parseFloat(document.getElementById("workout-weight").value) || null,
    calories_burned:
      parseFloat(document.getElementById("workout-calories").value) || null,
    notes: document.getElementById("workout-notes").value,
    completed: true,
  };

  try {
    await api.createWorkout(workoutData);
    alert("Treino registrado com sucesso!");
    document.getElementById("workout-form").reset();
    closeModal(document.getElementById("workout-modal"));
    loadDashboardData();
    loadWorkoutsData();
  } catch (error) {
    alert("Erro ao registrar treino: " + error.message);
  }
}

// Progress
async function loadProgressData() {
  try {
    const progress = await api.getUserProgress(appState.userId);
    const gallery = document.getElementById("progress-gallery");

    if (progress.length === 0) {
      gallery.innerHTML = "<p>Nenhuma foto de progresso registrada</p>";
    } else {
      gallery.innerHTML = progress
        .map(
          (p) => `
                <div class="photo-item">
                    ${
                      p.photo_url
                        ? `<img src="${p.photo_url}" alt="Progresso">`
                        : '<div style="background: #ddd; height: 200px; display: flex; align-items: center; justify-content: center;">Sem foto</div>'
                    }
                    <div class="photo-date">
                        <strong>${p.weight ? p.weight + " kg" : ""}</strong><br>
                        ${new Date(p.date).toLocaleDateString("pt-BR")}
                    </div>
                </div>
            `
        )
        .join("");
    }

    // Criar gráficos
    await updateAllCharts(appState.userId);
  } catch (error) {
    console.error("Error loading progress:", error);
  }
}

async function handleProgressSubmit(e) {
  e.preventDefault();

  const progressData = {
    user_id: appState.userId,
    weight: parseFloat(document.getElementById("progress-weight").value),
    photo_url: document.getElementById("progress-photo").value || null,
    notes: document.getElementById("progress-notes").value,
  };

  try {
    await api.logProgress(progressData);
    alert("Progresso registrado com sucesso!");
    document.getElementById("progress-form").reset();
    closeModal(document.getElementById("progress-modal"));
    loadProgressData();
    loadDashboardData();
  } catch (error) {
    alert("Erro ao registrar progresso: " + error.message);
  }
}

// Modal functions
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("active");
  }
}

function closeModal(modal) {
  if (modal) {
    modal.classList.remove("active");
  }
}

function showAuthModal() {
  const modal = document.getElementById("auth-modal");
  if (modal) {
    modal.classList.add("active");
    switchAuthTab("saved-users");
  }
}

function switchAuthTab(tabName) {
  const savedUsersTab = document.getElementById("saved-users-tab");
  const newUserTab = document.getElementById("new-user-tab");

  if (tabName === "saved-users") {
    savedUsersTab.classList.add("active");
    newUserTab.classList.remove("active");
  } else if (tabName === "new-user") {
    savedUsersTab.classList.remove("active");
    newUserTab.classList.add("active");
  }
}

function renderSavedUsers() {
  const usersList = document.getElementById("saved-users-list");
  if (!usersList) return;

  usersList.innerHTML = SAVED_USERS.map(
    (user) => `
        <div class="user-option" onclick="quickLogin('${user.email}', '${
      user.password
    }', '${user.name}')">
            <h4>${user.name}</h4>
            <div class="user-option-details">
                <span>📧 ${user.email}</span>
                <span>🎯 ${
                  user.objective === "ganho_massa"
                    ? "Ganho de Massa"
                    : user.objective === "perda_peso"
                    ? "Perda de Peso"
                    : "Tonificação"
                }</span>
                <span>📊 ${
                  user.level === "iniciante"
                    ? "Iniciante"
                    : user.level === "intermediario"
                    ? "Intermediário"
                    : "Avançado"
                }</span>
                <span>📅 ${user.days} dias/semana</span>
            </div>
        </div>
    `
  ).join("");
}

async function quickLogin(email, password, name) {
  try {
    // Sempre tenta fazer login com um usuário existente primeiro
    const user = await api.loginUser(email);

    // Se chegou aqui, usuário foi encontrado
    appState.currentUser = user;
    appState.userId = user.id;

    localStorage.setItem("userId", user.id);
    localStorage.setItem("userName", user.name);

    closeModal(document.getElementById("auth-modal"));
    updateUserName();
    loadUserData();
    showDashboard();
  } catch (error) {
    // Usuário não existe, tentar criar
    if (error.message.includes("User not found")) {
      try {
        const newUser = await api.createUser({
          name: name,
          email: email,
          password: password,
        });

        appState.currentUser = newUser;
        appState.userId = newUser.id;

        localStorage.setItem("userId", newUser.id);
        localStorage.setItem("userName", newUser.name);

        closeModal(document.getElementById("auth-modal"));
        updateUserName();
        loadUserData();
        showDashboard();
      } catch (createError) {
        alert("Erro ao criar conta: " + createError.message);
      }
    } else {
      alert("Erro ao fazer login: " + error.message);
    }
  }
}

// ==================== GAMIFICATION ====================

// Carregar stats de gamificação
async function loadGamificationStats(userId) {
  try {
    const stats = await api.getGamificationStats(userId);

    // Atualizar estatísticas
    const pointsEl = document.getElementById("points");
    if (pointsEl) pointsEl.textContent = stats.points.toLocaleString("pt-BR");

    const medalsCountEl = document.getElementById("medals-count");
    if (medalsCountEl) medalsCountEl.textContent = stats.total_medals;

    const workoutsEl = document.getElementById("workouts-count");
    if (workoutsEl) workoutsEl.textContent = stats.total_workouts;

    // Atualizar level
    const levelEl = document.getElementById("user-level");
    if (levelEl) levelEl.textContent = stats.level;

    // Atualizar progress bar
    const progressBar = document.getElementById("level-progress");
    if (progressBar) {
      progressBar.style.width = stats.progress_to_next_level + "%";
    }

    const levelPoints = document.getElementById("level-points");
    if (levelPoints) {
      const nextLevelPoints = stats.level * 500;
      levelPoints.textContent = `${stats.points} / ${nextLevelPoints} pontos`;
    }

    // Renderizar medalhas
    renderMedals(stats.medals);

    console.log("✅ Gamificação carregada:", stats);
    return stats;
  } catch (error) {
    console.error("❌ Erro ao carregar gamificação:", error);
  }
}

// Renderizar medalhas
function renderMedals(medals) {
  const container = document.getElementById("medals-container");
  if (!container) return;

  if (!medals || medals.length === 0) {
    container.innerHTML =
      '<p style="grid-column: 1/-1; text-align: center; color: #6b7280;">Complete treinos para ganhar medalhas! 🎯</p>';
    return;
  }

  const medalIcons = {
    bronze: "🥉",
    silver: "🥈",
    gold: "🥇",
  };

  const html = medals
    .map(
      (m) => `
        <div class="medal-item" title="${m.description}">
            <div class="medal-icon">${medalIcons[m.icon] || "🏅"}</div>
            <h4>${m.name}</h4>
            <p>${m.description}</p>
            <small>${new Date(m.earned_at).toLocaleDateString("pt-BR")}</small>
        </div>
    `
    )
    .join("");

  container.innerHTML = html;
}

// Atualizar dados do usuário
async function loadUserData() {
  if (!appState.userId) {
    console.warn("Nenhum userId definido");
    return;
  }

  try {
    console.log("📊 Carregando dados do usuário:", appState.userId);

    // Atualizar streak
    const streakEl = document.getElementById("streak");
    if (streakEl) streakEl.textContent = stats.streak + " dias";

    // Carregar gamificação
    await loadGamificationStats(appState.userId);

    // Carregar gráficos (se existir função)
    if (typeof updateAllCharts === "function") {
      await updateAllCharts(appState.userId);
    }
  } catch (error) {
    console.error("❌ Erro ao carregar dados:", error);
  }
}

// Chamar ao inicializar
document.addEventListener("DOMContentLoaded", () => {
  console.log("🎯 Inicializando...");

  // Se já tem userId logado, carregar dados
  if (appState && appState.userId) {
    loadUserData();
  }
});
