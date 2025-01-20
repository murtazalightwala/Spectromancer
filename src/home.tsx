
import React, {act, useEffect, useState} from 'react';
import { useNavigate } from 'react-router-dom';
import callAPI from './utils/callAPI';
import {setTokens} from './utils/auth';
import {GAME_LISTING_URLS} from './config/urls';


export default function HomePage()  {

    return (
<div className="HomePage"><p>This is Home Page</p> <GameTable/> </div>
    );
}


function GameTable() {

    const [games, setGames] = useState([]);

    useEffect(() => {

        const fetchGames = async () => {

            try {
            
                const data = await callAPI(GAME_LISTING_URLS.GET_GAMES, 'GET', {})

                setGames(data)
            }
            catch (error) {
 

                console.log("Error listing games", error);
            }
        };

        fetchGames();
    } 


    );
    

    return (
    <table className="GameTable">
            <tr>
                <th>Avatar</th>
                <th>Player</th>
                <th>Special</th>
            
            </tr>
        
        </table>
    );
}
