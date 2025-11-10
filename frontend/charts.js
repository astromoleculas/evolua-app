/**
 * Gerenciador de Gráficos - Evolua
 * Responsável por criar e atualizar gráficos de progresso
 */

let weightChart = null;
let workoutsChart = null;

/**
 * Cria/atualiza o gráfico de peso
 */
async function createWeightChart(userId) {
    try {
        const progress = await api.getUserProgress(userId);

        if (progress.length === 0) {
            displayNoDataMessage('weight-chart');
            return;
        }

        // Preparar dados
        const labels = progress.map(p =>
            new Date(p.date).toLocaleDateString('pt-BR', { month: 'short', day: 'numeric' })
        );
        const weights = progress.map(p => p.weight || 0);

        // Destruir gráfico anterior se existir
        if (weightChart) {
            weightChart.destroy();
        }

        const ctx = document.getElementById('weight-chart');
        if (!ctx) return;

        weightChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Peso (kg)',
                    data: weights,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#6366f1',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 6,
                    pointHoverRadius: 8,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: '#1f2937',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(31, 41, 55, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        padding: 12,
                        titleFont: {
                            size: 14,
                            weight: 'bold'
                        },
                        bodyFont: {
                            size: 13
                        },
                        cornerRadius: 4,
                        displayColors: true,
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Peso (kg)',
                            color: '#1f2937',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        },
                        ticks: {
                            color: '#6b7280',
                            font: {
                                size: 12
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)',
                        }
                    },
                    x: {
                        ticks: {
                            color: '#6b7280',
                            font: {
                                size: 12
                            }
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erro ao criar gráfico de peso:', error);
        displayNoDataMessage('weight-chart');
    }
}

/**
 * Cria/atualiza o gráfico de treinos
 */
async function createWorkoutsChart(userId) {
    try {
        const workouts = await api.getUserWorkouts(userId);

        if (workouts.length === 0) {
            displayNoDataMessage('workouts-chart');
            return;
        }

        // Agrupar treinos por semana
        const workoutsByWeek = {};
        const today = new Date();

        workouts.forEach(workout => {
            const workoutDate = new Date(workout.date);
            const weekStart = new Date(workoutDate);
            weekStart.setDate(workoutDate.getDate() - workoutDate.getDay());

            const weekKey = weekStart.toLocaleDateString('pt-BR', { month: 'short', day: 'numeric' });

            if (!workoutsByWeek[weekKey]) {
                workoutsByWeek[weekKey] = 0;
            }
            workoutsByWeek[weekKey]++;
        });

        // Preparar dados para gráfico
        const labels = Object.keys(workoutsByWeek);
        const data = Object.values(workoutsByWeek);

        // Destruir gráfico anterior se existir
        if (workoutsChart) {
            workoutsChart.destroy();
        }

        const ctx = document.getElementById('workouts-chart');
        if (!ctx) return;

        workoutsChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Treinos por Semana',
                    data: data,
                    backgroundColor: 'rgba(139, 92, 246, 0.8)',
                    borderColor: '#8b5cf6',
                    borderWidth: 2,
                    borderRadius: 6,
                    hoverBackgroundColor: 'rgba(139, 92, 246, 1)',
                }]
            },
            options: {
                indexAxis: 'x',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: '#1f2937',
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(31, 41, 55, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        padding: 12,
                        titleFont: {
                            size: 14,
                            weight: 'bold'
                        },
                        bodyFont: {
                            size: 13
                        },
                        cornerRadius: 4,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y + ' treino(s)';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: '#6b7280',
                            font: {
                                size: 12
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)',
                        }
                    },
                    x: {
                        ticks: {
                            color: '#6b7280',
                            font: {
                                size: 12
                            }
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Erro ao criar gráfico de treinos:', error);
        displayNoDataMessage('workouts-chart');
    }
}

/**
 * Exibe mensagem quando não há dados
 */
function displayNoDataMessage(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (canvas) {
        const parent = canvas.parentElement;
        parent.innerHTML = '<p style="text-align: center; color: #6b7280; padding: 2rem;">Nenhum dado disponível para exibir gráfico</p>';
    }
}

/**
 * Atualiza todos os gráficos
 */
async function updateAllCharts(userId) {
    await createWeightChart(userId);
    await createWorkoutsChart(userId);
}
