import React, { useEffect, useState } from 'react';
import style from './Carrinho.module.css';
import { api } from '../../services/api' 



export default function ShoppingList(){

    const [sellers, setSellers] = useState([]);
    const [clients, setClients] = useState([]);

    const [product, setProduct] = useState('');
    const [itemQuantity, setItemQuantity] = useState(0);
    const [item, setItemList] = useState([]);

    const [dataSales, setDataSales] = useState(0);

    const [setSeller, setSellerSelected] = useState([]);
    const [setClient, setClientSelected] = useState([]);


    useEffect(() => {
        async function loadSeller(){
            let response = await api.get('app/seller/');
            setSellers(response.data);  
        }

        loadSeller();
    },[]);

    useEffect(() => {
        async function loadClients() {
           let response = await api.get('app/clients/');
           setClients(response.data);
        }

        loadClients();
    },[])


    const formatCurrent = (value) => {
        let currentFormat =   new Intl.NumberFormat('pr-BR', {
            style: 'currency',
            currency: 'BRL',
            maximumSignificantDigits: 2}).format(value);
        return currentFormat + ',00';    
    }
    

    function handleAddProduct(event) {
        event.preventDefault();

        async function getProducts() {
            let response = await api.get(`app/product/${product}`);

            if (response.data.length !== 0) {
                
                const { id, produto, preco } = response.data[0];

                let total, price, subTotal, totalSale;

                total = preco * itemQuantity;
                price = formatCurrent(preco); 
                subTotal = formatCurrent(total);    
    
                let newProduct = {
                    'id':id,
                    'produto': produto,
                    'preco': price,
                    'quantidade': itemQuantity,
                    'subTotal': subTotal
                }
    
                setItemList([...item, newProduct]);

                totalSale = dataSales + total;
                setDataSales(totalSale);
                
               
            } else {
                alert('Nenhum resultado');
            }       
        }
        getProducts();       
    }
    
   
    function handleClearList() {
        setItemList([item - 1]);
        // setDataSales('');  
    }
    
    
   async function handleToSaveSalle(event) {
        event.preventDefault();

        const data = {
            "vendedor": setSeller,
            "cliente": setClient,
            "produto": product,
            "quantidade": itemQuantity,
            "subTotal": dataSales
        }

        await api.post('app/sales_list/add', data);
        
    }
   


    return (

        <div className={style.containerFlexrow}>
             <div className={style.contentLeft}>
                 <form action="" onSubmit='' method="get">
                   <h2>Produtos</h2> 
                     <div className={style.formGroup}>
                        <label htmlFor="">Buscar pelo código de barras ou descrição</label>
                        <input 
                           type="text" 
                           name="product" 
                           onChange={e => setProduct(e.target.value)}  
                           style={{ width: '400px'}} 
                           placeholder="Digite aqui o que procura" 
                        />
                    </div>

                    <div className={style.formGroup}>
                      <label htmlFor="">Quantidade de itens</label>
                      <input 
                           type="number" 
                           name="itens" min="1" 
                           onChange={e => setItemQuantity(e.target.value)}  
                           placeholder="Quantidade de itens"  
                        />
                    </div>

                    <div className={style.formGroup}>
                       <button 
                          type="submit" 
                          name="adicionar" 
                          onClick={handleAddProduct}>Adicionar</button>
                    </div>

                    <table>
                        <thead>
                            <tr>
                                <th>Produto/Serviço</th>
                                <th>Quantidade</th>
                                <th>Preço unitário</th>
                                <th>Total</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                        
                            {item.map(product => {

                               const { id, produto, preco, quantidade, subTotal } = product;
                                return (
                                 <>
                                   <tr id={id}>
                                     <td>{produto}</td>
                                     <td>{quantidade}</td>
                                     <td>{ preco}</td>
                                     <td>{ subTotal}</td>
                                     <td><i class="fas fa-trash" onClick={handleClearList}></i></td>
                                    </tr>
                                 </>
                                         
                                )
                            })}

                        </tbody>
                    </table>
                 </form>
             </div>

            <div className={style.contentRight}>    
                <form action="">
                    <h2>Dados da venda</h2>
                        <div className={style.formGroupSales}>
                          <label htmlFor="">Escolha um vendedor</label>
                            <select name="vendedor" id=""  onChange={e => setSellerSelected(e.target.value)} >
                                <option value="">Selecione o nome do vendedor</option>
                                {sellers.map(seller => {
                                    const { id, nome } = seller;
                                    return (
                                        <option id={id} value={nome}>{nome}</option>
                                    )    
                                    
                                })}
                                
                            </select>
                        </div>

                        <div className={style.formGroupSales} style={{ marginTop: '36px' }}>
                            <label htmlFor="">Escolha um cliente</label>
                            <select name="cliente" id="" onChange={e => setClientSelected(e.target.value)} >
                                <option value="">Selecione o nome do cliente</option>
                                {clients.map(client => {
                                    const { id, nome } = client;
                                    return (
                                        <option id={id} value={nome}>{nome}</option>
                                    )
                                })}
                            </select>
                        </div>

                        <div className={style.contentFooter}>
                            <div className={style.title}>
                                 <span>Valor total da venda</span>
                            </div>

                            <div className={style.valorTotal}>
                                {/* <p>R$ 136,10</p> */}

                                <p>{dataSales}</p>
                            </div>
                        </div>
                        <div className={style.buttons}>
                            <button 
                                  type="button" 
                                  name="cancelar" 
                                  className={style.cancelar}>
                                      Cancelar
                              </button>
                              <button 
                                 type="submit" 
                                 name="finalizar" 
                                 className={style.confirmar}
                                 onClick={handleToSaveSalle}
                               >Finalizar</button>
                        </div>
                    </form>
                </div>
          </div>

    )
}