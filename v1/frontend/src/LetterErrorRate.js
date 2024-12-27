import React, { useState, useEffect } from 'react';

// Chart stuff
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
  import { Bar } from 'react-chartjs-2';

function LetterErrorRate(props) {
    const [data, setData] = useState([]);

    useEffect(() => {
        getData().then(fetchedData => {
            setData(fetchedData);
        });
    }, [props.text]);

    const getData = () => {
        return fetch('http://127.0.0.1:44444/letter-error-rate')
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                return data;
            });
    };

    const options = {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Chart.js Bar Chart',
          },
        },
        scales: {
            y: {
                title: {
                    text: 'NumErrors',
                    display: true
                }
            },
            y1: {
                position: 'right',
                title: {
                    text: 'ErrorRate',
                    display: true
                }
            }
        }
    };

    ChartJS.register(
        CategoryScale,
        LinearScale,
        BarElement,
        Title,
        Tooltip,
        Legend
      );

    const graphData = {
        labels: data.chars,
        datasets: [
          {
            label: 'NumErrors',
            data: data.errorcounts,
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
          },
          {
            label: 'ErrorRate',
            data: data.percentages,
            backgroundColor: 'rgba(53, 162, 235, 0.5)',
          },
        ],
      };

    return (
        <Bar options={options} data={graphData} />
    );
}

export default LetterErrorRate;
