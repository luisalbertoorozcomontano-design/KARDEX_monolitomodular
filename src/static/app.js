const API = "";
const $ = (s, root=document) => root.querySelector(s);
const $$ = (s, root=document) => [...root.querySelectorAll(s)];
let session = null;
let cache = { fincas: [], parcelas: [], cosecheros: [], lotes: [], cosechas: [], movimientos: [] };
let currentPage = "dashboard";
const roleNames = {admin:"Encargado / Jefe", operador:"Trabajador de finca", consulta:"Cliente / Consulta"};
const navByRole = {
  admin: [["dashboard","▦","Resumen"],["lots","▤","Productos y lotes"],["movements","⇄","Movimientos Kardex"],["harvests","♧","Cosechas"],["workers","♙","Cosecheros"],["farms","⌂","Fincas y parcelas"]],
  operador: [["dashboard","▦","Mi espacio"],["harvests","♧","Registrar cosecha"],["lots","▤","Consultar lotes"]],
  consulta: [["dashboard","▦","Inicio"],["lots","▤","Catálogo de productos"],["movements","⇄","Movimientos recientes"]]
};
const today = () => new Date().toISOString().slice(0,10);
const fmt = n => Number(n||0).toLocaleString("es-BO",{maximumFractionDigits:3});
const safe = v => String(v ?? "").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function toast(message,error=false){const t=$("#toast");t.textContent=message;t.className="toast show"+(error?" error":"");clearTimeout(window.toastTimer);window.toastTimer=setTimeout(()=>t.className="toast",3600)}
async function request(path, options={}) {
  const response = await fetch(API+path,{...options,headers:{"Content-Type":"application/json",...(options.headers||{})}});
  const body = await response.json().catch(()=>({}));
  if(!response.ok) throw new Error(body.detail || body.msg || `Error ${response.status}`);
  return body;
}
function showAuth(tab="login"){
  $("#auth-screen").classList.remove("hidden");$("#app-shell").classList.add("hidden");
  $$(".tab").forEach(b=>b.classList.toggle("active",b.dataset.authTab===tab));
  $("#login-form-wrap").classList.toggle("hidden",tab!=="login");
  $("#register-form-wrap").classList.toggle("hidden",tab!=="register");
}
function showApp(){
  $("#auth-screen").classList.add("hidden");$("#app-shell").classList.remove("hidden");
  const name=session.nombre_completo||session.username;const initial=(name[0]||"U").toUpperCase();
  $("#side-user").textContent=name;$("#side-role").textContent=roleNames[session.rol]||session.rol;
  $("#user-avatar").textContent=initial;$("#top-avatar").textContent=initial;
  $("#today-label").textContent=new Intl.DateTimeFormat("es-BO",{dateStyle:"full"}).format(new Date());
  renderNav();loadData().then(()=>navigate("dashboard")).catch(e=>{toast(e.message,true);navigate("dashboard")});
}
function renderNav(){
  $("#side-nav").innerHTML=(navByRole[session.rol]||navByRole.consulta).map(([id,ico,label])=>`<button class="nav-item ${id===currentPage?"active":""}" data-page="${id}"><span class="nav-ico">${ico}</span>${label}</button>`).join("");
}
async function loadData(){
  const jobs=[["fincas","/inventario/fincas"],["parcelas","/inventario/parcelas"],["cosecheros","/cosecheros"],["lotes","/inventario/lotes"],["cosechas","/kardex/cosechas"],["movimientos","/kardex/movimientos"]];
  await Promise.all(jobs.map(async ([key,url])=>{try{cache[key]=await request(url)}catch(e){cache[key]=[];console.warn(url,e.message)}}));
}
function navigate(page){
  currentPage=page;renderNav();$("#page-crumb").textContent=({dashboard:"Resumen",lots:"Productos y lotes",movements:"Movimientos Kardex",harvests:"Cosechas",workers:"Cosecheros",farms:"Fincas y parcelas"})[page]||"Resumen";
  $("#sidebar").classList.remove("open");
  const views={dashboard:dashboardView,lots:lotsView,movements:movementsView,harvests:harvestsView,workers:workersView,farms:farmsView};
  $("#page-content").innerHTML=(views[page]||dashboardView)();
  bindPage();
}
function pageHead(kicker,title,desc,action=""){return `<div class="page-head"><div><div class="page-kicker">${kicker}</div><h1>${title}</h1><p>${desc}</p></div>${action}</div>`}
function stat(label,value,note,icon){return `<div class="stat-card"><div class="stat-top"><span>${label}</span><span class="stat-icon">${icon}</span></div><div class="stat-value">${value}</div><div class="stat-note">${note}</div></div>`}
function table(headers,rows,empty="Todavía no hay registros."){return `<div class="table-wrap"><table><thead><tr>${headers.map(h=>`<th>${h}</th>`).join("")}</tr></thead><tbody>${rows.length?rows.join(""):`<tr><td colspan="${headers.length}" class="empty">${empty}</td></tr>`}</tbody></table></div>`}
function dashboardView(){
 const isAdmin=session.rol==="admin",isWorker=session.rol==="operador";
 const kgHarvest=cache.cosechas.reduce((s,x)=>s+Number(x.kg||0),0);
 const stock=cache.movimientos.reduce((s,x)=>s+Number(x.entrada_kg||0)-Number(x.salida_kg||0),0);
 const cards=`<div class="cards">${stat("Cosechas registradas",cache.cosechas.length,"Registros de producción","♧")}${stat("Producción acumulada",fmt(kgHarvest)+" kg","Según cosechas registradas","↗")}${stat("Lotes registrados",cache.lotes.length,"Productos identificados","▤")}${stat("Existencia calculada",fmt(stock)+" kg","Entradas menos salidas registradas","◉")}</div>`;
 if(session.rol==="consulta")return `${pageHead("PORTAL DE CLIENTE","Bienvenido, "+safe(session.nombre_completo||session.username),"Consulta los productos y lotes disponibles en el inventario.")}<div class="client-banner"><span class="eyebrow">PORTAL DE CONSULTA</span><h2>Información clara, desde el origen.</h2><p>Explora los lotes registrados y consulta sus datos de ingreso.</p></div><div class="cards">${stat("Lotes publicados",cache.lotes.length,"En el catálogo","▤")}${stat("Fincas registradas",cache.fincas.length,"Origen de producción","⌂")}</div><div class="panel"><div class="panel-head"><div><h3>Productos recientes</h3><p>Últimos lotes incorporados al sistema</p></div><button class="btn btn-soft" data-go="lots">Ver catálogo</button></div>${lotsTable()}</div>`;
 if(isWorker)return `${pageHead("ESPACIO DEL TRABAJADOR","Hola, "+safe(session.nombre_completo||session.username),"Registra tu producción y consulta la información de lotes.")}<div class="cards">${stat("Cosechas registradas",cache.cosechas.length,"Registros del sistema","♧")}${stat("Producción acumulada",fmt(kgHarvest)+" kg","Kilogramos registrados","↗")}${stat("Fincas",cache.fincas.length,"Fincas disponibles","⌂")}${stat("Lotes",cache.lotes.length,"Lotes registrados","▤")}</div><div class="panel"><div class="panel-head"><div><h3>Acciones de trabajo</h3><p>Operaciones disponibles para el perfil trabajador</p></div></div><div class="quick-actions"><button class="quick-action" data-go="harvests"><span class="quick-ico">♧</span><strong>Registrar cosecha</strong><span>Ingresar fecha, finca, parcela y kilogramos.</span></button><button class="quick-action" data-go="lots"><span class="quick-ico">▤</span><strong>Consultar lotes</strong><span>Revisar lotes existentes.</span></button></div></div>`;
 return `${pageHead("PANEL DE CONTROL","Resumen general","Indicadores principales de producción e inventario.",'<button class="btn btn-primary" data-go="lots">＋ Agregar producto</button>')}${cards}<div class="grid-two"><div class="panel"><div class="panel-head"><div><h3>Últimas cosechas</h3><p>Actividad reciente de producción</p></div><button class="btn btn-soft" data-go="harvests">Ver todas</button></div>${harvestsTable(5)}</div><div class="panel"><div class="panel-head"><div><h3>Accesos rápidos</h3><p>Administración del sistema</p></div></div><div class="quick-actions" style="grid-template-columns:1fr 1fr"><button class="quick-action" data-go="lots"><span class="quick-ico">＋</span><strong>Agregar producto</strong><span>Registrar un lote.</span></button><button class="quick-action" data-go="movements"><span class="quick-ico">⇄</span><strong>Movimiento</strong><span>Registrar entrada o salida.</span></button><button class="quick-action" data-go="workers"><span class="quick-ico">♙</span><strong>Cosecheros</strong><span>Gestionar trabajadores.</span></button><button class="quick-action" data-go="farms"><span class="quick-ico">⌂</span><strong>Fincas</strong><span>Gestionar fincas.</span></button></div></div></div>`;
}
function lotsTable(){
 const rows=cache.lotes.slice().reverse().map(l=>`<tr><td><b>${safe(l.codigo)}</b></td><td>${safe(l.fecha_ingreso)}</td><td>${safe(l.finca_id??"—")}</td><td>${safe(l.detalle||"—")}</td><td><span class="pill">Registrado</span></td></tr>`);
 return table(["CÓDIGO DE LOTE","FECHA DE INGRESO","FINCA ID","DETALLE","ESTADO"],rows,"No hay lotes registrados todavía.");
}
function lotsView(){
 const canManage=session.rol==="admin";
 return `${pageHead("INVENTARIO","Productos y lotes","Consulta los productos ingresados y registra nuevos lotes.",canManage?'<button class="btn btn-primary" data-scroll="lot-form">＋ Agregar producto</button>':"")}
 <div class="panel"><div class="panel-head"><div><h3>Catálogo de productos</h3><p>Los productos se representan mediante lotes de ingreso en el modelo actual.</p></div><span class="pill">${cache.lotes.length} lotes</span></div>${lotsTable()}</div>
 ${canManage?`<div class="panel" id="lot-form"><div class="panel-head"><div><h3>Agregar producto / lote</h3><p>Registra el lote y, después, registra su entrada en el Kardex.</p></div></div><form id="create-lot-form"><div class="form-grid"><label class="field">Código de lote<input name="codigo" placeholder="Ej. TVH194E" required maxlength="30"></label><label class="field">Fecha de ingreso<input type="date" name="fecha_ingreso" value="${today()}" required></label><label class="field">Finca<select name="finca_id"><option value="">Sin finca asignada</option>${cache.fincas.map(f=>`<option value="${f.id}">${safe(f.nombre||"Finca "+f.numero)} (#${f.id})</option>`).join("")}</select></label><label class="field">Detalle / producto<input name="detalle" placeholder="Ej. Hoja fresca"></label></div><div class="form-actions"><button class="btn btn-primary">Guardar lote</button></div></form></div>`:""}`;
}
function harvestsTable(limit=100){
 const rows=cache.cosechas.slice().reverse().slice(0,limit).map(c=>{const w=cache.cosecheros.find(x=>x.id===c.cosechero_id);const f=cache.fincas.find(x=>x.id===c.finca_id);return `<tr><td>${safe(c.fecha)}</td><td>${safe(w?.nombre||("#"+c.cosechero_id))}</td><td>${safe(f?.nombre||("Finca "+(f?.numero??c.finca_id)))}</td><td><b>${fmt(c.kg)} kg</b></td><td>Bs ${fmt(c.monto_bs)}</td></tr>`});
 return table(["FECHA","COSECHERO","FINCA","CANTIDAD","MONTO"],rows,"No hay cosechas registradas.");
}
function harvestsView(){
 const isWorker=session.rol==="operador",canCreate=session.rol!=="consulta";
 return `${pageHead("PRODUCCIÓN","Registro de cosechas","Control de producción por cosechero, finca y parcela.")}
 ${canCreate?`<div class="panel"><div class="panel-head"><div><h3>Registrar nueva cosecha</h3><p>Completa los datos de producción para guardar el registro.</p></div></div>${cache.cosecheros.length&&cache.fincas.length?"":'<div class="notice-inline">Para registrar una cosecha primero deben existir al menos un cosechero y una finca. Solicita al encargado que los registre.</div>'}<form id="create-harvest-form"><div class="form-grid"><label class="field">Fecha<input type="date" name="fecha" value="${today()}" required></label><label class="field">Cosechero<select name="cosechero_id" required><option value="">Seleccionar cosechero</option>${cache.cosecheros.filter(x=>x.activo!==false).map(x=>`<option value="${x.id}">${safe(x.nombre)}</option>`).join("")}</select></label><label class="field">Finca<select name="finca_id" required><option value="">Seleccionar finca</option>${cache.fincas.map(x=>`<option value="${x.id}">${safe(x.nombre||"Finca "+x.numero)}</option>`).join("")}</select></label><label class="field">Parcela<select name="parcela_id"><option value="">Sin parcela</option>${cache.parcelas.map(x=>`<option value="${x.id}">Parcela ${x.numero} · Finca ${x.finca_id}</option>`).join("")}</select></label><label class="field">Tipo de cosecha<input name="tipo_cosecha" value="HOJA FRESCA" required></label><label class="field">Cantidad (kg)<input name="kg" type="number" min="0.001" step="0.001" required></label><label class="field">Monto (Bs)<input name="monto_bs" type="number" min="0" step="0.01" value="0"></label><label class="field span-2">Observación<input name="observacion" maxlength="200" placeholder="Observaciones opcionales"></label></div><div class="form-actions"><button class="btn btn-primary" ${!cache.cosecheros.length||!cache.fincas.length?"disabled":""}>Guardar cosecha</button></div></form></div>`:""}
 <div class="panel"><div class="panel-head"><div><h3>Historial de cosechas</h3><p>Registros almacenados en la base de datos.</p></div></div>${harvestsTable()}</div>`;
}
function movementsView(){
 const canManage=session.rol==="admin";
 const rows=cache.movimientos.slice().reverse().map(m=>`<tr><td>${safe(m.fecha)}</td><td>${safe(m.detalle)}</td><td>${safe(m.doc||"—")}</td><td>${fmt(m.entrada_kg)} kg</td><td>${fmt(m.salida_kg)} kg</td><td><b>${fmt(m.saldo_kg)} kg</b></td></tr>`);
 return `${pageHead("CONTROL DE EXISTENCIAS","Movimientos Kardex","Historial de entradas, salidas y saldos.")}
 ${canManage?`<div class="panel"><div class="panel-head"><div><h3>Registrar movimiento</h3><p>Registra una entrada o salida de inventario.</p></div></div><form id="create-movement-form"><div class="form-grid"><label class="field">Fecha<input type="date" name="fecha" value="${today()}" required></label><label class="field">Detalle<input name="detalle" placeholder="Ej. Ingreso de producto" required maxlength="150"></label><label class="field">Documento<input name="doc" placeholder="N.º de documento"></label><label class="field">Lote<select name="lote_id"><option value="">Sin lote</option>${cache.lotes.map(l=>`<option value="${l.id}">${safe(l.codigo)}</option>`).join("")}</select></label><label class="field">Finca<select name="finca_id"><option value="">Sin finca</option>${cache.fincas.map(f=>`<option value="${f.id}">${safe(f.nombre||"Finca "+f.numero)}</option>`).join("")}</select></label><label class="field">Entrada (kg)<input name="entrada_kg" type="number" min="0" step="0.001" value="0"></label><label class="field">Salida (kg)<input name="salida_kg" type="number" min="0" step="0.001" value="0"></label><label class="field">Observación<input name="observacion" placeholder="Opcional"></label></div><div class="notice-inline">El saldo que muestra el backend se calcula a partir del último saldo general. Para una operación real se debe validar el stock por lote y evitar salidas superiores a las existencias.</div><div class="form-actions"><button class="btn btn-primary">Guardar movimiento</button></div></form></div>`:""}
 <div class="panel"><div class="panel-head"><div><h3>Libro de movimientos</h3><p>Información consultada desde kardex_movimientos.</p></div></div>${table(["FECHA","DETALLE","DOCUMENTO","ENTRADA","SALIDA","SALDO"],rows,"No hay movimientos registrados.")}</div>`;
}
function workersView(){
 if(session.rol!=="admin")return dashboardView();
 const rows=cache.cosecheros.map(w=>`<tr><td>${safe(w.nombre)}</td><td>${safe(w.ci||"—")}</td><td>${safe(w.telefono||"—")}</td><td><span class="pill ${w.activo?"":"gray"}">${w.activo?"Activo":"Inactivo"}</span></td></tr>`);
 return `${pageHead("PERSONAL","Cosecheros","Administra las personas que realizan las labores de cosecha.")}<div class="panel"><div class="panel-head"><div><h3>Registrar cosechero</h3><p>El registro de cosechero es independiente de la cuenta de acceso al sistema.</p></div></div><form id="create-worker-form"><div class="form-grid"><label class="field">Nombre completo<input name="nombre" required></label><label class="field">Cédula de identidad<input name="ci"></label><label class="field">Teléfono<input name="telefono"></label></div><div class="form-actions"><button class="btn btn-primary">Guardar cosechero</button></div></form></div><div class="panel"><div class="panel-head"><h3>Personal registrado</h3><span class="pill">${cache.cosecheros.length} personas</span></div>${table(["NOMBRE","CI","TELÉFONO","ESTADO"],rows)}</div>`;
}
function farmsView(){
 if(session.rol!=="admin")return dashboardView();
 const frows=cache.fincas.map(f=>`<tr><td>${safe(f.numero)}</td><td>${safe(f.nombre||"—")}</td><td>${safe(f.ubicacion||"—")}</td><td>${cache.parcelas.filter(p=>p.finca_id===f.id).length}</td></tr>`);
 const prows=cache.parcelas.map(p=>`<tr><td>${safe(p.numero)}</td><td>${safe(p.finca_id)}</td><td>${safe(p.superficie_ha??"—")} ha</td></tr>`);
 return `${pageHead("ESTRUCTURA AGRÍCOLA","Fincas y parcelas","Organiza los espacios de producción agrícola.")}<div class="grid-two"><div class="panel"><div class="panel-head"><h3>Registrar finca</h3></div><form id="create-farm-form"><div class="form-grid"><label class="field">Número<input name="numero" type="number" min="1" required></label><label class="field">Nombre<input name="nombre"></label><label class="field span-2">Ubicación<input name="ubicacion"></label></div><div class="form-actions"><button class="btn btn-primary">Guardar finca</button></div></form><div style="margin-top:22px">${table(["N.º","NOMBRE","UBICACIÓN","PARCELAS"],frows)}</div></div><div class="panel"><div class="panel-head"><h3>Registrar parcela</h3></div><form id="create-plot-form"><div class="form-grid"><label class="field">Finca<select name="finca_id" required><option value="">Seleccionar</option>${cache.fincas.map(f=>`<option value="${f.id}">${safe(f.nombre||"Finca "+f.numero)}</option>`).join("")}</select></label><label class="field">Número<input name="numero" type="number" min="1" required></label><label class="field span-2">Superficie (ha)<input name="superficie_ha" type="number" min="0" step="0.01"></label></div><div class="form-actions"><button class="btn btn-primary">Guardar parcela</button></div></form><div style="margin-top:22px">${table(["PARCELA","FINCA ID","SUPERFICIE"],prows)}</div></div></div>`;
}
function formObject(form){const o=Object.fromEntries(new FormData(form).entries());Object.keys(o).forEach(k=>{if(o[k]==="")o[k]=null});return o}
function num(o,keys){keys.forEach(k=>{if(o[k]!==null)o[k]=Number(o[k])});return o}
function bindPage(){
 $$("[data-page]").forEach(b=>b.addEventListener("click",()=>navigate(b.dataset.page)));
 $$("[data-go]").forEach(b=>b.addEventListener("click",()=>navigate(b.dataset.go)));
 $$("[data-scroll]").forEach(b=>b.addEventListener("click",()=>$("#"+b.dataset.scroll)?.scrollIntoView({behavior:"smooth"})));
 const bind=async(id,url,transform= x=>x,success="Registro guardado correctamente.")=>{const f=$("#"+id);if(!f)return;f.addEventListener("submit",async e=>{e.preventDefault();try{await request(url,{method:"POST",body:JSON.stringify(transform(formObject(f)))});toast(success);await loadData();navigate(currentPage)}catch(err){toast(err.message,true)}})};
 bind("create-lot-form","/inventario/lotes",o=>({...o,finca_id:o.finca_id?Number(o.finca_id):null}),"Lote registrado. Ahora puedes registrar su entrada en el Kardex.");
 bind("create-harvest-form","/kardex/cosechas",o=>({...o,...num(o,["cosechero_id","finca_id","parcela_id","kg","monto_bs"])}),"Cosecha registrada correctamente.");
 bind("create-movement-form","/kardex/movimientos",o=>({...o,...num(o,["lote_id","finca_id","entrada_kg","salida_kg"]),saldo_kg:0}),"Movimiento registrado correctamente.");
 bind("create-worker-form","/cosecheros",o=>o,"Cosechero registrado.");
 bind("create-farm-form","/inventario/fincas",o=>({...o,numero:Number(o.numero)}),"Finca registrada.");
 bind("create-plot-form","/inventario/parcelas",o=>({...o,...num(o,["finca_id","numero","superficie_ha"])}),"Parcela registrada.");
}
$$(".tab").forEach(b=>b.addEventListener("click",()=>showAuth(b.dataset.authTab)));
$("#login-form").addEventListener("submit",async e=>{
 e.preventDefault();const o=formObject(e.currentTarget);
 try{const data=await request("/auth/login",{method:"POST",body:JSON.stringify(o)});session={username:data.usuario,rol:data.rol,nombre_completo:data.nombre_completo||data.usuario};if(!roleNames[session.rol])throw new Error("El perfil de esta cuenta no tiene una interfaz configurada.");localStorage.setItem("kardex-demo-session",JSON.stringify(session));showApp()}
 catch(err){toast(err.message,true)}
});
$("#register-form").addEventListener("submit",async e=>{
 e.preventDefault();const o=formObject(e.currentTarget);
 if(String(o.password).length<6){toast("La contraseña debe tener al menos 6 caracteres.",true);return}
 try{await request("/auth/register",{method:"POST",body:JSON.stringify(o)});toast("Cuenta creada. Ahora puedes iniciar sesión.");e.currentTarget.reset();showAuth("login");$("#login-form [name=username]").value=o.username}
 catch(err){toast(err.message,true)}
});
$("#logout-btn").addEventListener("click",()=>{session=null;localStorage.removeItem("kardex-demo-session");showAuth("login")});
$("#menu-toggle").addEventListener("click",()=>$("#sidebar").classList.toggle("open"));
(async function init(){
 try{const saved=JSON.parse(localStorage.getItem("kardex-demo-session")||"null");if(saved&&roleNames[saved.rol]){session=saved;showApp()}else showAuth("login")}catch(e){showAuth("login")}
})();
