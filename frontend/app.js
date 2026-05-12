/**
 * EVOLUA - Aplicação Principal
 * SPA que gerencia todo o fluxo de usuário
 */

class EvoluaApp {
    constructor() {
        this.currentUser = null;
        this.currentPlan = null;
        this.currentWorkout = null;
        this.currentWorkoutId = null;
        this.currentPage = 'login';
        this.workoutTimer = null;
        this.workoutStartTime = null;
        
        this.init();
    }

    init() {
        this.checkAuth();
        this.render();
        this.attachEventListeners();
    }

    checkAuth() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            this.currentPage = 'login';
        } else {
            this.currentPage = 'dashboard';
            this.loadUserData();
        }
    }

    async loadUserData() {
        try {
            const profile = await api.getProfile();
            this.currentUser = profile;
            // Carregar dados do dashboard após carregar perfil
            if (this.currentPage === 'dashboard') {
                this.loadDashboard();
            }
        } catch (error) {
            console.error('Erro ao carregar perfil:', error);
            this.logout();
        }
    }

    // ==================== RENDER ====================

    render() {
        const app = document.getElementById('app');
        app.innerHTML = this.getPageHTML();
        this.attachEventListeners();
    }

    getPageHTML() {
        switch (this.currentPage) {
            case 'login':
                return this.getLoginHTML();
            case 'register':
                return this.getRegisterHTML();
            case 'dashboard':
                return this.getDashboardHTML();
            case 'workout':
                return this.getWorkoutHTML();
            case 'progress':
                return this.getProgressHTML();
            case 'medals':
                return this.getMedalsHTML();
            case 'profile':
                return this.getProfileHTML();
            default:
                return this.getLoginHTML();
        }
    }

    // ==================== PÁGINAS ====================

    getLoginHTML() {
        return `
            <div class="auth-container">
                <div class="auth-card">
                    <div class="auth-header">
                        <h1>🏋️ EVOLUA</h1>
                        <p>Seu Personal Trainer Digital</p>
                    </div>
                    
                    <form id="login-form" class="auth-form">
                        <input type="email" id="login-email" placeholder="Email" required>
                        <input type="password" id="login-password" placeholder="Senha" required>
                        <button type="submit" class="btn btn-primary btn-full">Entrar</button>
                    </form>
                    
                    <div class="auth-divider">ou</div>
                    
                    <button class="btn btn-secondary btn-full" id="go-to-register">Criar Conta</button>
                    
                    <div class="demo-info">
                        <p><strong>Demo:</strong> Email: demo@evolua.com | Senha: demo123</p>
                    </div>
                </div>
            </div>
        `;
    }

    getRegisterHTML() {
        return `
            <div class="auth-container">
                <div class="auth-card">
                    <div class="auth-header">
                        <h1>🏋️ EVOLUA</h1>
                        <p>Comece sua transformação</p>
                    </div>
                    
                    <form id="register-form" class="auth-form">
                        <input type="text" id="register-name" placeholder="Nome Completo" required>
                        <input type="email" id="register-email" placeholder="Email" required>
                        <input type="password" id="register-password" placeholder="Senha (min. 6 caracteres)" required>
                        
                        <select id="register-objective" required>
                            <option value="">Selecione seu objetivo</option>
                            <option value="hipertrofia">Ganho de Massa</option>
                            <option value="perda_peso">Perda de Peso</option>
                            <option value="tonificacao">Tonificação</option>
                        </select>
                        
                        <select id="register-level" required>
                            <option value="">Qual é seu nível?</option>
                            <option value="iniciante">Iniciante</option>
                            <option value="intermediario">Intermediário</option>
                            <option value="avancado">Avançado</option>
                        </select>
                        
                        <button type="submit" class="btn btn-primary btn-full">Criar Conta</button>
                    </form>
                    
                    <button class="btn btn-secondary btn-full" id="go-to-login" style="margin-top: 10px;">Voltar ao Login</button>
                </div>
            </div>
        `;
    }

    getDashboardHTML() {
        return `
            <nav class="navbar">
                <div class="navbar-brand">🏋️ EVOLUA</div>
                <div class="navbar-menu">
                    <button class="nav-btn" data-page="dashboard">Dashboard</button>
                    <button class="nav-btn" data-page="progress">Progresso</button>
                    <button class="nav-btn" data-page="medals">Medalhas</button>
                    <button class="nav-btn" data-page="profile">Perfil</button>
                    <button class="nav-btn logout-btn" id="logout-btn">Sair</button>
                </div>
            </nav>
            
            <div class="container">
                <div class="dashboard">
                    <div class="dashboard-header">
                        <h1>Bem-vindo, ${this.currentUser?.name || 'Usuário'}! 👋</h1>
                        <p>${new Date().toLocaleDateString('pt-BR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
                    </div>
                    
                    <div class="stats-grid" id="stats-container">
                        <div class="stat-card">
                            <div class="stat-value" id="points-display">0</div>
                            <div class="stat-label">Pontos</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="workouts-display">0</div>
                            <div class="stat-label">Treinos Completos</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="streak-display">0</div>
                            <div class="stat-label">Dias Consecutivos</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value" id="medals-display">0</div>
                            <div class="stat-label">Medalhas</div>
                        </div>
                    </div>
                    
                    <div class="dashboard-content">
                        <div class="section">
                            <h2>Seu Plano de Treino</h2>
                            <div id="plans-container" class="plans-list">
                                <div class="loading">Carregando planos...</div>
                            </div>
                        </div>
                        
                        <div class="section">
                            <h2>Últimos Treinos</h2>
                            <div id="workouts-container" class="workouts-list">
                                <div class="loading">Carregando histórico...</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getWorkoutHTML() {
        if (!this.currentWorkout) {
            return '<div class="container"><p>Carregando treino...</p></div>';
        }

        return `
            <nav class="navbar">
                <button class="btn btn-small" id="back-from-workout">← Voltar</button>
                <span>Treino em Andamento</span>
                <div id="workout-timer">00:00</div>
            </nav>
            
            <div class="container">
                <div class="workout-session">
                    <h1>${this.currentWorkout.name}</h1>
                    <div class="focus-group">${this.currentWorkout.focus}</div>
                    
                    <div class="exercises-list" id="exercises-container">
                        <!-- Exercícios carregados via JS -->
                    </div>
                    
                    <div class="workout-actions">
                        <button class="btn btn-success btn-full" id="finish-workout">Finalizar Treino</button>
                    </div>
                </div>
            </div>
        `;
    }

    getProgressHTML() {
        return `
            <nav class="navbar">
                <div class="navbar-brand">🏋️ EVOLUA</div>
                <button class="btn btn-small" id="back-from-progress">← Dashboard</button>
            </nav>
            
            <div class="container">
                <div class="progress-section">
                    <h1>Seu Progresso 📊</h1>
                    
                    <div class="progress-input">
                        <h3>Registrar Progresso</h3>
                        <form id="progress-form">
                            <input type="number" id="weight-input" placeholder="Peso (kg)" step="0.01">
                            <textarea id="progress-notes" placeholder="Notas (opcional)"></textarea>
                            <button type="submit" class="btn btn-primary btn-full">Registrar Progresso</button>
                        </form>
                    </div>
                    
                    <div id="progress-charts">
                        <div class="chart-container">
                            <canvas id="weight-chart"></canvas>
                        </div>
                    </div>
                    
                    <div id="progress-history">
                        <h3>Histórico</h3>
                        <div id="history-container" class="history-list">
                            <!-- Histórico carregado via JS -->
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getMedalsHTML() {
        return `
            <nav class="navbar">
                <div class="navbar-brand">🏋️ EVOLUA</div>
                <button class="btn btn-small" id="back-from-medals">← Dashboard</button>
            </nav>
            
            <div class="container">
                <div class="medals-section">
                    <h1>Suas Medalhas 🏆</h1>
                    <div id="medals-container" class="medals-grid">
                        <div class="loading">Carregando medalhas...</div>
                    </div>
                </div>
            </div>
        `;
    }

    getProfileHTML() {
        return `
            <nav class="navbar">
                <div class="navbar-brand">🏋️ EVOLUA</div>
                <button class="btn btn-small" id="back-from-profile">← Dashboard</button>
            </nav>
            
            <div class="container">
                <div class="profile-section">
                    <h1>Seu Perfil 👤</h1>
                    
                    <form id="profile-form" class="profile-form">
                        <div class="form-group">
                            <label>Nome</label>
                            <input type="text" id="profile-name" value="${this.currentUser?.name || ''}" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Email</label>
                            <input type="email" id="profile-email" value="${this.currentUser?.email || ''}" disabled>
                        </div>
                        
                        <div class="form-group">
                            <label>Idade</label>
                            <input type="number" id="profile-age" value="${this.currentUser?.age || ''}" min="15" max="100">
                        </div>
                        
                        <div class="form-group">
                            <label>Objetivo</label>
                            <select id="profile-objective" required>
                                <option value="hipertrofia" ${this.currentUser?.objective === 'hipertrofia' ? 'selected' : ''}>Ganho de Massa</option>
                                <option value="perda_peso" ${this.currentUser?.objective === 'perda_peso' ? 'selected' : ''}>Perda de Peso</option>
                                <option value="tonificacao" ${this.currentUser?.objective === 'tonificacao' ? 'selected' : ''}>Tonificação</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label>Nível</label>
                            <select id="profile-level" required>
                                <option value="iniciante" ${this.currentUser?.level === 'iniciante' ? 'selected' : ''}>Iniciante</option>
                                <option value="intermediario" ${this.currentUser?.level === 'intermediario' ? 'selected' : ''}>Intermediário</option>
                                <option value="avancado" ${this.currentUser?.level === 'avancado' ? 'selected' : ''}>Avançado</option>
                            </select>
                        </div>
                        
                        <button type="submit" class="btn btn-primary btn-full">Salvar Alterações</button>
                    </form>
                </div>
            </div>
        `;
    }

    // ==================== EVENT LISTENERS ====================

    attachEventListeners() {
        // Login
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        // Register
        const registerForm = document.getElementById('register-form');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }

        // Navigation
        document.querySelectorAll('[data-page]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const page = e.target.dataset.page;
                this.currentPage = page;
                if (page === 'dashboard') {
                    this.loadDashboard();
                } else if (page === 'progress') {
                    this.loadProgress();
                } else if (page === 'medals') {
                    this.loadMedals();
                }
                this.render();
            });
        });

        // Logout
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }

        // Page navigation
        document.getElementById('go-to-register')?.addEventListener('click', () => {
            this.currentPage = 'register';
            this.render();
        });

        document.getElementById('go-to-login')?.addEventListener('click', () => {
            this.currentPage = 'login';
            this.render();
        });

        // Progress form
        const progressForm = document.getElementById('progress-form');
        if (progressForm) {
            progressForm.addEventListener('submit', (e) => this.handleProgressSubmit(e));
        }

        // Profile form
        const profileForm = document.getElementById('profile-form');
        if (profileForm) {
            profileForm.addEventListener('submit', (e) => this.handleProfileSubmit(e));
        }

        // Back buttons
        document.getElementById('back-from-progress')?.addEventListener('click', () => {
            this.currentPage = 'dashboard';
            this.render();
            this.loadDashboard();
        });

        document.getElementById('back-from-medals')?.addEventListener('click', () => {
            this.currentPage = 'dashboard';
            this.render();
            this.loadDashboard();
        });

        document.getElementById('back-from-profile')?.addEventListener('click', () => {
            this.currentPage = 'dashboard';
            this.render();
            this.loadDashboard();
        });

        document.getElementById('back-from-workout')?.addEventListener('click', () => {
            this.currentPage = 'dashboard';
            this.stopWorkoutTimer();
            this.render();
            this.loadDashboard();
        });

        // Finish workout button
        const finishWorkoutBtn = document.getElementById('finish-workout');
        if (finishWorkoutBtn) {
            finishWorkoutBtn.addEventListener('click', (e) => this.handleFinishWorkout(e));
        }
    }

    // ==================== HANDLERS ====================

    async handleLogin(e) {
        e.preventDefault();
        
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        try {
            await api.login(email, password);
            await this.loadUserData();
            this.currentPage = 'dashboard';
            this.loadDashboard();
            this.render();
        } catch (error) {
            alert('Erro no login: ' + error.message);
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        
        const name = document.getElementById('register-name').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const objective = document.getElementById('register-objective').value;
        const level = document.getElementById('register-level').value;

        try {
            await api.register(name, email, password, objective, level);
            await api.createPlan(); // Criar plano automático
            await this.loadUserData();
            this.currentPage = 'dashboard';
            this.loadDashboard();
            this.render();
        } catch (error) {
            alert('Erro no registro: ' + error.message);
        }
    }

    async handleProgressSubmit(e) {
        e.preventDefault();
        
        const weight = parseFloat(document.getElementById('weight-input').value);
        const notes = document.getElementById('progress-notes').value;

        if (!weight || isNaN(weight)) {
            alert('Por favor, insira um peso válido');
            return;
        }

        try {
            const response = await api.logProgress(weight, {}, null, notes);
            
            if (response.updated) {
                alert('✅ Progresso do dia já foi atualizado com sucesso!\nNota: Apenas um registro de peso por dia é permitido.');
            } else {
                alert('✅ Progresso registrado com sucesso!');
            }
            
            document.getElementById('progress-form').reset();
            this.loadProgress();
        } catch (error) {
            alert('❌ Erro ao registrar progresso: ' + error.message);
        }
    }

    async handleProfileSubmit(e) {
        e.preventDefault();
        
        const data = {
            name: document.getElementById('profile-name').value,
            age: parseInt(document.getElementById('profile-age').value),
            objective: document.getElementById('profile-objective').value,
            level: document.getElementById('profile-level').value
        };

        try {
            await api.updateProfile(data);
            await this.loadUserData();
            alert('Perfil atualizado com sucesso!');
            this.currentPage = 'dashboard';
            this.render();
        } catch (error) {
            alert('Erro ao atualizar perfil: ' + error.message);
        }
    }

    async handleFinishWorkout(e) {
        e.preventDefault();
        
        if (!this.currentWorkoutId) {
            alert('Erro: ID do treino não encontrado');
            return;
        }
        
        try {
            const durationMinutes = Math.floor((new Date() - this.workoutStartTime) / 60000);
            
            await api.completeWorkout(this.currentWorkoutId, durationMinutes);
            
            alert('Treino finalizado! +50 pontos 🎉');
            this.stopWorkoutTimer();
            this.currentWorkoutId = null;
            this.currentWorkout = null;
            this.currentPage = 'dashboard';
            this.render();
            this.loadDashboard();
        } catch (error) {
            console.error('Erro ao finalizar treino:', error);
            alert('Erro ao finalizar treino: ' + error.message);
        }
    }

    // ==================== DATA LOADING ====================

    async loadDashboard() {
        try {
            const stats = await api.getStats();
            document.getElementById('points-display').textContent = stats.points;
            document.getElementById('workouts-display').textContent = stats.workouts_completed;
            document.getElementById('streak-display').textContent = stats.current_streak;
            document.getElementById('medals-display').textContent = stats.medals;

            const plans = await api.getPlans();
            const plansContainer = document.getElementById('plans-container');
            
            if (plans.length === 0) {
                plansContainer.innerHTML = '<button class="btn btn-primary" id="create-plan">Criar Plano de Treino</button>';
                document.getElementById('create-plan')?.addEventListener('click', async () => {
                    await api.createPlan();
                    this.loadDashboard();
                });
            } else {
                plansContainer.innerHTML = plans.map(plan => `
                    <div class="plan-card">
                        <h3>${plan.name}</h3>
                        <p>${plan.description}</p>
                        <button class="btn btn-secondary btn-full" data-plan-id="${plan.id}">Ver Detalhes</button>
                    </div>
                `).join('');

                document.querySelectorAll('[data-plan-id]').forEach(btn => {
                    btn.addEventListener('click', async (e) => {
                        const planId = e.target.dataset.planId;
                        this.currentPlan = await api.getPlanDetails(planId);
                        this.showPlanDetails();
                    });
                });
            }

            const workouts = await api.getUserWorkouts();
            const workoutsContainer = document.getElementById('workouts-container');
            
            if (workouts.length === 0) {
                workoutsContainer.innerHTML = '<p>Nenhum treino registrado ainda.</p>';
            } else {
                workoutsContainer.innerHTML = workouts.slice(0, 5).map(w => `
                    <div class="workout-card ${w.completed ? 'completed' : ''}">
                        <div class="workout-date">${new Date(w.date).toLocaleDateString('pt-BR')}</div>
                        <div class="workout-info">
                            <span>${w.duration_minutes} min</span> | <span>${w.exercises_count} exercícios</span>
                            ${w.completed ? '<span class="badge">✓ Completo</span>' : ''}
                        </div>
                    </div>
                `).join('');
            }
        } catch (error) {
            console.error('Erro ao carregar dashboard:', error);
        }
    }

    async loadProgress() {
        try {
            const history = await api.getProgressHistory();
            const container = document.getElementById('history-container');
            
            // Ordenar por data crescente (do passado para hoje)
            const sortedHistory = [...history].sort((a, b) => new Date(a.date) - new Date(b.date));
            
            if (sortedHistory.length === 0) {
                container.innerHTML = '<p>Nenhum registro de progresso ainda.</p>';
            } else {
                container.innerHTML = sortedHistory.map(h => `
                    <div class="progress-record" data-progress-id="${h.id}">
                        <div class="progress-record-content">
                            <div class="record-date">${new Date(h.date).toLocaleDateString('pt-BR')}</div>
                            <div class="record-weight">${h.weight !== null ? parseFloat(h.weight).toFixed(2) : '0.00'} kg</div>
                            ${h.notes ? `<div class="record-notes">${h.notes}</div>` : ''}
                        </div>
                        <button class="btn btn-small edit-progress-btn" data-progress-id="${h.id}" data-weight="${h.weight}" data-date="${h.date}" data-notes="${h.notes || ''}">✏️ Editar</button>
                    </div>
                `).join('');
                
                // Adicionar event listeners para botões de editar
                document.querySelectorAll('.edit-progress-btn').forEach(btn => {
                    btn.addEventListener('click', (e) => this.showEditProgressModal(e));
                });
            }

            // Renderizar gráfico de peso (com dados ordenados)
            this.renderWeightChart(sortedHistory);
        } catch (error) {
            console.error('Erro ao carregar progresso:', error);
        }
    }

    async showEditProgressModal(e) {
        const progressId = e.target.dataset.progressId;
        const weight = e.target.dataset.weight;
        const date = e.target.dataset.date;
        const notes = e.target.dataset.notes;
        
        const formattedDate = new Date(date).toLocaleDateString('pt-BR');
        
        // Criar modal
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Editar Progresso - ${formattedDate}</h3>
                    <button class="modal-close">✕</button>
                </div>
                <div class="modal-body">
                    <form id="edit-progress-form">
                        <div class="form-group">
                            <label for="edit-weight-input">Peso (kg)</label>
                            <input type="number" id="edit-weight-input" value="${weight}" step="0.01" required>
                        </div>
                        <div class="form-group">
                            <label for="edit-notes-input">Notas (opcional)</label>
                            <textarea id="edit-notes-input">${notes}</textarea>
                        </div>
                        <div class="modal-actions">
                            <button type="submit" class="btn btn-primary">Salvar Alterações</button>
                            <button type="button" class="btn" id="cancel-edit">Cancelar</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Event listeners do modal
        modal.querySelector('.modal-close').addEventListener('click', () => modal.remove());
        modal.querySelector('#cancel-edit').addEventListener('click', () => modal.remove());
        
        modal.querySelector('#edit-progress-form').addEventListener('submit', async (ev) => {
            ev.preventDefault();
            const newWeight = document.getElementById('edit-weight-input').value;
            const newNotes = document.getElementById('edit-notes-input').value;
            
            try {
                // Atualizar via API
                await api.updateProgress(progressId, newWeight, newNotes);
                modal.remove();
                // Recarregar os dados do progresso
                await this.loadProgress();
            } catch (error) {
                console.error('Erro ao atualizar progresso:', error);
                alert('Erro ao atualizar o progresso');
            }
        });
    }

    async loadMedals() {
        try {
            const medals = await api.getMedals();
            const container = document.getElementById('medals-container');
            
            if (medals.length === 0) {
                container.innerHTML = '<p>Você ainda não conquistou nenhuma medalha. Comece a treinar!</p>';
            } else {
                container.innerHTML = medals.map(m => `
                    <div class="medal-card medal-${m.icon}">
                        <div class="medal-icon">🏅</div>
                        <div class="medal-name">${m.name}</div>
                        <div class="medal-description">${m.description}</div>
                        <div class="medal-date">${new Date(m.earned_at).toLocaleDateString('pt-BR')}</div>
                    </div>
                `).join('');
            }
        } catch (error) {
            console.error('Erro ao carregar medalhas:', error);
        }
    }

    showPlanDetails() {
        const weeks = this.currentPlan.weeks || [];
        let html = `<div class="plan-details"><h3>${this.currentPlan.name}</h3>`;
        
        weeks.forEach(week => {
            html += `<div class="week"><h4>Semana ${week.number}</h4>`;
            
            week.sessions.forEach(session => {
                html += `
                    <div class="session">
                        <h5>${session.name}</h5>
                        <button class="btn btn-primary" data-session-id="${session.id}">Iniciar Treino</button>
                    </div>
                `;
            });
            
            html += '</div>';
        });
        
        html += '</div>';
        
        const container = document.getElementById('plans-container');
        container.innerHTML = html;

        document.querySelectorAll('[data-session-id]').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const sessionId = e.target.dataset.sessionId;
                await this.startWorkout(sessionId);
            });
        });
    }

    async startWorkout(sessionId) {
        try {
            // Encontrar a sessão nos dados
            const week = this.currentPlan.weeks[0];
            const session = week.sessions.find(s => s.id == sessionId);
            
            if (session) {
                // Criar novo workout na API
                const workoutData = await api.createWorkout(sessionId);
                this.currentWorkoutId = workoutData.workout_id;
                
                this.currentWorkout = session;
                this.currentPage = 'workout';
                this.workoutStartTime = new Date();
                this.startWorkoutTimer();
                this.render();
                this.renderWorkoutExercises();
            }
        } catch (error) {
            console.error('Erro ao iniciar treino:', error);
            alert('Erro ao iniciar treino: ' + error.message);
        }
    }

    renderWorkoutExercises() {
        const container = document.getElementById('exercises-container');
        if (!this.currentWorkout || !this.currentWorkout.exercises) return;

        container.innerHTML = this.currentWorkout.exercises.map((exc, idx) => `
            <div class="exercise-card">
                <div class="exercise-header">
                    <h3>${exc.name}</h3>
                    <span class="exercise-number">${idx + 1}/${this.currentWorkout.exercises.length}</span>
                </div>
                
                <div class="exercise-info">
                    <span>${exc.sets} séries x ${exc.reps} reps</span>
                    <span>${exc.rest_seconds}s descanso</span>
                </div>
                
                <div class="exercise-input">
                    <input type="number" placeholder="Série 1 (reps)" class="exercise-reps" data-exercise-id="${exc.id}">
                </div>
                
                <button class="btn btn-success" data-exercise-idx="${idx}" data-exercise-id="${exc.id}">Completo ✓</button>
            </div>
        `).join('');

        document.querySelectorAll('.btn-success').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const exerciseId = e.target.dataset.exerciseId;
                const exerciseIdx = parseInt(e.target.dataset.exerciseIdx);
                const card = e.target.parentElement;
                const reps = card.querySelector('.exercise-reps').value;
                
                try {
                    if (this.currentWorkoutId && exerciseId && reps) {
                        await api.logExercise(
                            this.currentWorkoutId,
                            exerciseId,
                            1,
                            reps,
                            null,
                            'normal'
                        );
                        
                        e.target.parentElement.style.opacity = '0.6';
                        e.target.disabled = true;
                        e.target.textContent = 'Completado ✓';
                    } else {
                        alert('Preencha o número de repetições');
                    }
                } catch (error) {
                    console.error('Erro ao registrar exercício:', error);
                    alert('Erro ao registrar exercício: ' + error.message);
                }
            });
        });
    }

    startWorkoutTimer() {
        this.workoutTimer = setInterval(() => {
            const elapsed = Math.floor((new Date() - this.workoutStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            const timerEl = document.getElementById('workout-timer');
            if (timerEl) {
                timerEl.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
            }
        }, 1000);
    }

    stopWorkoutTimer() {
        if (this.workoutTimer) {
            clearInterval(this.workoutTimer);
            this.workoutTimer = null;
        }
    }

    renderWeightChart(history) {
        const canvas = document.getElementById('weight-chart');
        if (!canvas || history.length === 0) return;

        const ctx = canvas.getContext('2d');
        const data = {
            labels: history.map(h => new Date(h.date).toLocaleDateString('pt-BR')),
            datasets: [{
                label: 'Peso (kg)',
                data: history.map(h => h.weight !== null ? parseFloat(h.weight).toFixed(2) : 0),
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                tension: 0.4,
                fill: true
            }]
        };

        new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true }
                },
                scales: {
                    y: { 
                        beginAtZero: false,
                        ticks: {
                            color: '#000000'
                        },
                        grid: {
                            color: '#e0e0e0'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#000000'
                        },
                        grid: {
                            color: '#e0e0e0'
                        }
                    }
                }
            }
        });
    }

    logout() {
        api.logout();
        this.currentUser = null;
        this.currentPage = 'login';
        this.render();
    }
}

// Inicializar app quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.app = new EvoluaApp();
});
