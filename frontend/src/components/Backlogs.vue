<script setup>
  import { ref, watch, computed } from "vue";
  import draggable from "vuedraggable";
  import { useRoute } from "vue-router";
  import axios from "axios";
  import router from "@/router";

  // Import chart components
  import { Pie, Bar } from "vue-chartjs";
  import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale } from "chart.js";

  ChartJS.register(Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale);

  const route = useRoute();

  const projectId = ref(route.params.id);

  // Project details
  const project = ref({
    title: "",
    description: "",
  });

  const sprints_data = ref([]);
  const task_data = ref([]);

  // Reactive state
  const sprints = ref([]);

  // Backend base URL from environment variables
  const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;

  // Total backlogs and completed backlogs
  const totalBacklogs = computed(() => {
    return sprints.value.reduce((total, sprint) => total + sprint.tasks.length, 0);
  });

  const completedBacklogs = computed(() => {
    return sprints.value.reduce(
      (total, sprint) =>
        total + sprint.tasks.filter((task) => task.status === "completed").length,
      0
    );
  });

  const backlogPercentage = computed(() => {
    return totalBacklogs.value > 0
      ? Math.round((completedBacklogs.value / totalBacklogs.value) * 100)
      : 0;
  });

  // Task Progress Chart Data
  const taskProgressBarChartData = computed(() => {
    const toDo = task_data.value.filter((task) => task.status === "to_do").length;
    const inProgress = task_data.value.filter((task) => task.status === "in_progress").length;
    const completed = task_data.value.filter((task) => task.status === "completed").length;
    const under_review = task_data.value.filter((task) => task.status === "under_review").length;

    return {
      labels: ["To Do", "In Progress", "Under review", "Completed"],
      datasets: [
        {
            label: "Task Progress",
          data: [toDo, inProgress, under_review, completed],
            backgroundColor: ["#FF5722","#FFC107", "#2196F3", "#4CAF50"],
          borderRadius: 5,
        },
      ],
    };
  });

  const taskProgressBarChartOptions = {
    plugins: {
      title: {
        display: false, // Disable the title at the top
      },
      legend: {
        display: false, // Optionally hide the legend if not needed
      },
    },
    responsive: true,
    maintainAspectRatio: false,
  };

  // Metrics Breakdown Chart Data
  const metricsChartData = computed(() => {
    const environmental = task_data.value.filter((task) => task.impact.includes("environmental")).length;
    const economic = task_data.value.filter((task) => task.impact.includes("economic")).length;
    const social = task_data.value.filter((task) => task.impact.includes("social")).length;
    const individual = task_data.value.filter((task) => task.impact.includes("individual")).length;
    const technical = task_data.value.filter((task) => task.impact.includes("technical")).length;

    console.log(environmental, economic, social);

    return {
      labels: ["Environmental", "Economic", "Social", "Individual", "Technical"],
      datasets: [
        {
          data: [environmental, economic, social, individual, technical],
          backgroundColor: ["#4CAF50", "#FFC107", "#2196F3", "#FF5722", "#9C27B0"],
        },
      ],
    };
  });

  // Task Sentiment Chart Data
  const taskSentimentChartData = computed(() => {
    const positive = task_data.value.filter((task) => task.type === "positive").length;
    const negative = task_data.value.filter((task) => task.type === "negative").length;

    return {
      labels: ["Positive", "Negative"],
      datasets: [
        {
          data: [positive, negative],
          backgroundColor: ["#4CAF50", "#F44336"],
        },
      ],
    };
  });

  // process the display data for sprints and tasks
  // Watcher
  function processData() {
    console.log(sprints_data.value, task_data.value);
    for (const sprint_data of sprints_data.value) {
      const sprint = {
        id: sprint_data.id,
        name: sprint_data.title,
        editing: false,
        tasks: [],
      };
      for (let i = 0; i < task_data.value.length; i++) {
        if (task_data.value[i].sprint == sprint.id) {
          const task = { id: task_data.value[i].id, 
                        name: task_data.value[i].title, 
                        status : task_data.value[i].status,
                        type : task_data.value[i].type,
                        impacts : task_data.value[i].impact, 
                      };
          sprint.tasks.push(task);
        }
      }
      sprints.value.push(sprint);
      console.log(sprints.value);
    }
  }

  // Watch for route changes and re-fetch data
  watch(
    () => route.params.id,
    (newId) => {
      projectId.value = parseInt(newId, 10); // Update projectId as an integer
      sprints_data.value = []; // Clear existing data
      task_data.value = [];
      sprints.value = [];
      get_project(); // Re-fetch data for the new project ID
      console.log(projectId.value);
    }
  );

  // Methods
  async function get_project() {
    try {
      const response = await axios.get(`${backendBaseUrl}/susaf/projects/${projectId.value}`);
      project.value.title = response.data.name;
      project.value.description = response.data.description;

      await get_sprints(projectId.value);
    } catch (error) {
      console.error(error);
      alert(error);
    }
  }

  async function get_sprints(project_id) {
    try {
      const response = await axios.get(`${backendBaseUrl}/susaf/sprints/`);
      for (const sprint of response.data) {
        if (sprint.project == project_id) {
          sprints_data.value.push(sprint);
          console.log(sprint.data);
        }
      }
      const resp = await get_tasks();
    } catch (error) {
      console.error(error);
      alert(error);
    }
  }

  async function get_tasks() {
    try {
      const response = await axios.get(`${backendBaseUrl}/susaf/tasks/`);
      for (const task of response.data) {
        // Loop through each sprint in sprints_data
        for (let i = 0; i < sprints_data.value.length; i++) {
          // Check if task's sprint matches the current sprint
          if (sprints_data.value[i].id == task.sprint) {
            task_data.value.push(task); // Push the task into task_data
          }
        }
      }

      processData(); // Call the function to process and display data
    } catch (error) {
      console.error(error);
      alert(error);
    }
  }

  get_project();

  const addSprint = async () => {
    let new_sprint = await axios.post(`${backendBaseUrl}/susaf/sprints/`, {
      title: "Untitled Sprint",
      project: projectId.value,
    });

    sprints.value.push({
      id: new_sprint.data.id,
      name: new_sprint.data.title,
      editing: false,
      tasks: [],
    });
  };

  const editSprint = (sprint) => {
    sprint.editing = true;
  };

  const stopEditing = async (sprint) => {
    sprint.editing = false;

    try {
      // Update the sprint in the database
      await axios.put(`${backendBaseUrl}/susaf/sprints/${sprint.id}/`, {
        title: sprint.name,
        project: projectId.value,
      });
    } catch (error) {
      console.error("Error updating sprint:", error);
      alert("Failed to update the sprint. Please try again.");
    }
  };

  const goToTaskDetail = (taskId) => {
    router.push({ name: "detail", params: { id: taskId } });
  };

  const updateTaskSprint = async (taskId, newSprintId) => {
    try {
      await axios.patch(`${backendBaseUrl}/susaf/tasks/${taskId}/`, {
        sprint: newSprintId,
      });
      console.log(`Task ${taskId} moved to sprint ${newSprintId}`);
    } catch (error) {
      console.error("Error updating task sprint:", error);
      alert("Failed to update task's sprint.");
    }
  };

  const onTaskDrop = async (event, newSprintId, event_to) => {
    console.log(event_to);
    const task = event.item.querySelector(".task-name");
    const taskId = task.id;

    const sprint = event_to.querySelector(".task");
    const sprintId = sprint.getAttribute("sprint_id");

    if (taskId && sprintId) {
      await updateTaskSprint(taskId, sprintId);
    }
  };
</script>

<template>
  <div class="dashboard-container">
    <!-- Backlogs Section -->
    <div class="backlogs-section">
      <div class="title-container">
        <h3 class="title">{{ project.title }}</h3>
        <div class="jira-icon-container">
          <img src="@/assets/images/jira.svg" alt="Jira Icon" class="jira-icon" />
          <div class="tooltip">Export project to Jira</div>
        </div>
      </div>

      <div class="subtitle-container">
        <!-- First Section: Project Description -->
        <div class="description-section">
          <p class="subtitle">{{ project.description }}</p>
        </div>

        <!-- Second Section: Fancy Cards -->
        <div class="cards-section">
          <!-- Total Sprints Card -->
          <div class="card">
            <p class="card-title">Number of Sprints</p>
            <p class="card-value">{{ sprints.length }}</p>
          </div>

          <!-- Completed Backlogs Card -->
          <div class="card">
            <p class="card-title">Backlogs completed</p>
            <p class="card-value">
              {{ completedBacklogs }} / {{ totalBacklogs }}
              <span class="percentage">({{ backlogPercentage }}%)</span>
            </p>
          </div>
        </div>
      </div>

      <div v-for="sprint in sprints" :key="sprint.id" class="sprint-box">
        <!-- Editable Sprint Title -->
        <input
          v-if="sprint.editing"
          v-model="sprint.name"
          @blur="stopEditing(sprint)"
          @keyup.enter="stopEditing(sprint)"
          class="sprint-title-input"
        />
        <h4 v-else class="sprint-title" @click="editSprint(sprint)">{{ sprint.name }}</h4>

        <!-- Draggable Task List -->
        <draggable
          v-model="sprint.tasks"
          group="tasks"
          itemKey="id"
          class="task-list"
          @end="(event) => onTaskDrop(event, sprint.id, event.to)"
        >
          <template #item="{ element: task }">
            <div class="task" :sprint_id="sprint.id" @click="goToTaskDetail(task.id)">
              <span class="task-name" :id="task.id">{{ task.name }}</span>
            </div>
          </template>
        </draggable>
      </div>

      <div class="footer">
        <button class="add-sprint" @click="addSprint">+ Add New Sprint</button>
      </div>
    </div>

    <!-- Visualizations Section -->
    <div class="visualizations-section">
      <!-- Task Progress Bar Chart -->
      <div class="chart bar-chart">
        <h4>Task Progress</h4>
        <Bar :data="taskProgressBarChartData" :options="taskProgressBarChartOptions" />
      </div>

      <!-- Other Charts -->
      <div class="chart">
        <h4>Metrics Breakdown</h4>
        <Pie :data="metricsChartData" />
      </div>
      <div class="chart">
        <h4>Task Sentiment</h4>
        <Pie :data="taskSentimentChartData" />
      </div>
    </div>
  </div>
</template>

<style scoped>
  /* Container */
  .dashboard-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 96%;
    margin: auto;
    padding: 2%;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.1);
    text-align: left;
  }

  .backlogs-section {
    width: 62%;
  }

  .visualizations-section {
    width: 35%; /* Reduced from 30% to 25% */
    padding-left: 0px;
  }

  .chart {
    margin-bottom: 20px;
    width: 100%; /* Ensure charts take up the full width of their container */
    max-width: 400px; /* Set a maximum width for the charts */
    margin: 10px auto; /* Center the charts horizontally */
    margin-bottom: 50px;
  }

  .chart h4{
    text-align: center;
    margin-bottom: 10px;
  }

  .bar-chart {
    margin-bottom: 50px;
    width: 100%; /* Ensure it takes the full width of its container */
    max-width: 600px; /* Increase the maximum width */
    height: 350px; /* Set a fixed height for the bar chart */
    margin: 0 auto; /* Center the chart horizontally */
    margin-bottom: 80px;
  }

  /* Title */
  .title {
    font-size: 35px;
    color: #353535;
    font-family: "Poppins";
    font-weight: 600;
    margin-bottom: 10px;
  }

  .subtitle {
    margin-bottom: 10px;
    text-align: justify;
    color: rgb(50, 50, 50);
    font-family: "Poppins", sans-serif;
  }

  .title-container {
    display: flex;
    align-items: center;
    gap: 50px;
  }

  .jira-icon-container {
    position: relative;
    display: inline-block;
    cursor: pointer;
    transition: transform 0.3s ease-in-out;
  }

  .jira-icon-container:hover {
    transform: scale(1.1); /* Micro-interaction: Slight scaling */
  }

  .jira-icon-container:hover .tooltip {
    opacity: 1;
    visibility: visible;
    transform: translateY(-10px); /* Smooth upward animation */
  }

  .jira-icon {
    width: 30px;
    height: 30px;
  }

  .tooltip {
    position: absolute;
    bottom: 100%; /* Position above the icon */
    left: 50%;
    transform: translateX(-50%) translateY(0);
    background-color: #333;
    color: #fff;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 12px;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease, transform 0.3s ease;
    z-index: 10;
  }

  /* Sprint Box */
  .sprint-box {
    background: linear-gradient(135deg, rgba(245, 245, 245, 1), white);
    padding: 25px;
    margin: 20px 0;
    border-radius: 10px;
    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease-in-out;
  }

  .sprint-box:hover {
    transform: translateY(-5px);
  }

  /* Editable Sprint Title */
  .sprint-title {
    font-size: 20px;
    font-weight: 600;
    cursor: pointer;
    transition: color 0.3s ease;
    margin-bottom: 20px;
    border-bottom: 1px solid #ccc;
    padding-bottom: 10px;
    color: #555555;
  }

  .sprint-title:hover {
    color: #007bff;
    color: #333833;
  }

  .sprint-title-input {
    font-size: 20px;
    font-weight: 600;
    width: 100%;
    border: none;
    background: none;
    outline: none;
    padding: 5px;
  }

  /* Task List */
  .task-list {
    min-height: 50px;
  }

  /* Task */
  .task {
    background: #fafafa;
    padding: 12px 15px;
    margin: 10px 0;
    display: flex;
    align-items: center;
    border-radius: 8px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
    transition: background 0.3s ease-in-out;
    cursor: pointer;
    color: rgb(50, 50, 50);
    font-family: "Poppins", sans-serif;
  }

  .task:hover {
    background: #f1f1f1;
  }

  /* Add Sprint Button */
  .add-sprint {
    background: #007bff;
    color: white;
    font-size: 16px;
    padding: 12px 20px;
    border: none;
    cursor: pointer;
    border-radius: 8px;
    transition: background 0.3s ease-in-out;
    margin-top: 20px;
  }

  .add-sprint:hover {
    background: #0056b3;
  }

  /* Subtitle Container */
  .subtitle-container {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .description-section {
    width: 55%;
  }

  .cards-section {
    width: 35%;
    display: flex;
    flex-direction: row;
    gap: 20px;
    margin-top: -60px;
    margin-bottom: 0px;
  }

  .card {
    padding: 30px 15px;
    border-radius: 12px;
    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    width: 50%;
    text-align: center;
  }

  .card .card-title {
    font-size: 14px;
    font-weight: 500;
    color: rgba(32, 34, 36, 1);
    margin-bottom: 10px;
    font-family: "Nunito Sans", sans-serif;
  }

  .card-value {
    font-size: 24px;
    font-weight: 700;
    color: rgba(32, 34, 36, 1);
    font-family: "Nunito Sans", sans-serif;
  }

  .percentage {
    font-size: 14px;
    font-weight: 500;
    color: #4caf50;
  }
</style>
