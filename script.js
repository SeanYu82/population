// Supabase configuration
const SUPABASE_URL = 'https://gkklkjoatvbxfekuyvnx.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdra2xram9hdHZieGZla3V5dm54Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMzNjAzMTgsImV4cCI6MjA3ODkzNjMxOH0.UNVFvR7yOTe1pmowWa4s6LPuj4FOZTo85mCwRCBAzHE';

// Initialize Supabase client
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Chart instance
let populationChart = null;

// Initialize the application
const init = () => {
    setupEventListeners();
    initializeChart();
};

// Setup event listeners
const setupEventListeners = () => {
    const searchForm = document.querySelector('#searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', handleFormSubmit);
    }
};

// Handle form submission
const handleFormSubmit = async (event) => {
    event.preventDefault();
    
    const districtCodeInput = document.querySelector('#districtCode');
    const dateInput = document.querySelector('#date');
    const alertMessage = document.querySelector('#alertMessage');
    
    const districtCode = districtCodeInput.value.trim();
    const date = dateInput.value.trim();
    
    // Clear previous alert
    clearAlert();
    
    // Validate inputs
    if (!districtCode || !date) {
        showAlert('올바른 값을 입력해주세요.', 'error');
        return;
    }
    
    // Validate district code format (should be numeric)
    if (!/^\d+$/.test(districtCode)) {
        showAlert('행정동코드는 숫자만 입력 가능합니다.', 'error');
        return;
    }
    
    try {
        // Fetch data from Supabase
        const data = await fetchPopulationData(districtCode, date);
        
        if (data && data.length > 0) {
            updateChart(data);
            showAlert('데이터를 성공적으로 조회했습니다.', 'success');
        } else {
            showAlert('조회된 데이터가 없습니다.', 'warning');
            clearChart();
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        showAlert('데이터 조회 중 오류가 발생했습니다.', 'error');
        clearChart();
    }
};

// Fetch population data from Supabase
const fetchPopulationData = async (districtCode, date) => {
    // Convert district code to number for proper comparison (BIGINT in database)
    const districtCodeNum = parseInt(districtCode, 10);
    
    if (isNaN(districtCodeNum)) {
        throw new Error('Invalid district code format');
    }
    
    const { data, error } = await supabase
        .from('seoul_population')
        .select('time_hour, total_population')
        .eq('district_code', districtCodeNum)
        .eq('date', date)
        .order('time_hour', { ascending: true });
    
    if (error) {
        throw error;
    }
    
    return data;
};

// Initialize Chart.js
const initializeChart = () => {
    const ctx = document.querySelector('#populationChart');
    if (!ctx) return;
    
    const config = {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: '총생활인구수',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: '시간대별 총생활인구수 추이'
                },
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '시간대 (시)'
                    },
                    ticks: {
                        stepSize: 1
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '총생활인구수'
                    },
                    beginAtZero: false
                }
            }
        }
    };
    
    populationChart = new Chart(ctx, config);
};

// Update chart with new data
const updateChart = (data) => {
    if (!populationChart) return;
    
    // Sort by time_hour to ensure correct order (database returns sorted, but double-check)
    const sortedData = [...data].sort((a, b) => a.time_hour - b.time_hour);
    
    const labels = sortedData.map(item => `${item.time_hour}시`);
    // total_population is NUMERIC type, may be returned as string, so parse to float
    const populationData = sortedData.map(item => {
        const value = parseFloat(item.total_population);
        if (isNaN(value)) {
            console.warn('Invalid population value:', item.total_population);
            return 0;
        }
        return value;
    });
    
    populationChart.data.labels = labels;
    populationChart.data.datasets[0].data = populationData;
    populationChart.update();
};

// Clear chart
const clearChart = () => {
    if (!populationChart) return;
    
    populationChart.data.labels = [];
    populationChart.data.datasets[0].data = [];
    populationChart.update();
};

// Show alert message
const showAlert = (message, type = 'info') => {
    const alertMessage = document.querySelector('#alertMessage');
    if (!alertMessage) return;
    
    alertMessage.textContent = message;
    alertMessage.className = `alert-message alert-${type}`;
    alertMessage.style.display = 'block';
    
    // Auto-hide success messages after 3 seconds
    if (type === 'success') {
        setTimeout(() => {
            clearAlert();
        }, 3000);
    }
};

// Clear alert message
const clearAlert = () => {
    const alertMessage = document.querySelector('#alertMessage');
    if (!alertMessage) return;
    
    alertMessage.textContent = '';
    alertMessage.className = 'alert-message';
    alertMessage.style.display = 'none';
};

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
