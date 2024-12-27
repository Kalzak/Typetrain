import React, { useState, useEffect } from 'react';

function WordPassFailRate(props) {
    const [data, setData] = useState([]);

    useEffect(() => {
        getData().then(fetchedData => {
            setData(fetchedData);
        });
    }, [props.text]);

    const getData = () => {
        return fetch('http://127.0.0.1:44444/word-pass-fail-ratio')
            .then((response) => response.json())
            .then((data) => {
                return data;
            });
    };

    return (
        <div className="m-4">
            <table className="w-full text-sm border border-collapse">
                <thead>
                    <tr className="bg-gray-100">
                        <th className="border px-3 py-1">Word</th>
                        <th className="border px-3 py-1">Fails</th>
                        <th className="border px-3 py-1">Passes</th>
                        <th className="border px-3 py-1">Fail%</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item, index) => (
                        <tr key={index}>
                            <td className="border px-3 py-0">{item.word}</td>
                            <td className="border px-3 py-0">{item.fails}</td>
                            <td className="border px-3 py-0">{item.passes}</td>
                            <td className="border px-3 py-0">{((item.fails / (item.passes + item.fails))*100).toFixed(1)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default WordPassFailRate;
