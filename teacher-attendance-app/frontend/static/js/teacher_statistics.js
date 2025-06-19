document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});

function initializeCharts() {
    const departmentData = window.statsData?.department_chart_data;
    if (departmentData && departmentData.labels) {
        const departmentCtx = document.getElementById('departmentChart').getContext('2d');
        new Chart(departmentCtx, {
            type: 'pie',
            data: {
                labels: departmentData.labels,
                datasets: [{
                    data: departmentData.data,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }

    const degreeData = window.statsData?.degree_chart_data;
    if (degreeData && degreeData.labels) {
        const degreeCtx = document.getElementById('degreeChart').getContext('2d');
        new Chart(degreeCtx, {
            type: 'doughnut',
            data: {
                labels: degreeData.labels,
                datasets: [{
                    data: degreeData.data,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}
