import React, { useState, useEffect } from 'react';

function WeakSubstrings(props) {
    const [data, setData] = useState({ substrings: [], frequency: [] });

    useEffect(() => {
        getData().then(fetchedData => {
            setData(fetchedData);
        });
    }, [props.text]);

    const getData = () => {
        return fetch('http://127.0.0.1:44444/get-weak-substrings')
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                return data;
            });
            
    };

    /*
    return (
        <div className="m-4">
            <table className="w-full text-sm border border-collapse">
                <thead>
                    <tr className="bg-gray-100">
                        <th className="border px-3 py-1">Substring</th>
                        <th className="border px-3 py-1">Fails</th>
                    </tr>
                </thead>
                <tbody>
                    {data.substrings.map((substring, index) => (
                        <tr key={index}>
                            <td className="border px-3 py-0">{substring.replace(" ", "_")}</td>
                            <td className="border px-3 py-0">{data.frequency[index]}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
    */

    let structured_data = [];

    let i = 0;

    let j = 0;
    for(j; j < 5; j++) {
        structured_data.push([]);
        let k = 0;
        for(k; k < 18; k++) {
            structured_data[j].push(data.substrings[i]);
            i++;
            if(data.substrings.length == i) {
                break;
            }
        }
        if(data.substrings == i) {
            break;
        }
    }

    return (
        <div className="m-4" style={{ display: 'flex', flexWrap: 'wrap', maxWidth: '100%' }}>
            {structured_data.map((column, colIndex) => (
                <div key={colIndex} style={{ flex: '1', maxWidth: '25%' }}>
                    <table className="text-sm border border-collapse" style={{ marginBottom: '20px' }}>
                        
                        <thead>
                            <tr className="bg-gray-100">
                                <th className="border px-3 py-1">Substring</th>
                                <th className="border px-3 py-1">Fails</th>
                            </tr>
                        </thead>
                        
                        <tbody>
                            {column.map((substring, index) => (
                                <tr key={index}>
                                    {substring && <td className="border px-3 py-0">{substring.replace(" ", "_")}</td>}
                                    <td className="border px-3 py-0">{data.frequency[data.substrings.indexOf(substring)]}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ))}
        </div>
    );
}

export default WeakSubstrings;