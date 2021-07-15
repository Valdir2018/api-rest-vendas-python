import React from 'react';
import logoIpsum from '../assets/images/logoipsum-logo-7.svg';

import style from  './Header.module.css';

export default function Header() {
    return (
      <div className={style.containerFlexrow}>
         <header class={style.topo}>
            <img src={logoIpsum} alt="" />
            <div>Caixa livre</div>
         </header>
      </div>
    )
}