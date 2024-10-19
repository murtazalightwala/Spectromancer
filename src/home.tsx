
import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import callAPI from './utils/callAPI';
import {setTokens} from './utils/auth';


export default function HomePage()  {

    return (
<div className="HomePage"><p>This is Home Page</p> <GameTable/> </div>
    );
}


function GameTable() {


    return (
    <table className="GameTable">
            <tr>
                <th>Avatar</th>
                <th>Player</th>
                <th>Special</th>

            </tr></table>
    );
}
