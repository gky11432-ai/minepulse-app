# ui_part3.py - DGMS Statutory Form UI Component

PART3 = """
    <!-- STATUTORY FORM VIEW -->
    <div id="vf" class="hidden space-y-4">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 max-w-3xl mx-auto shadow-xl">
        <div class="border-b border-slate-800 pb-3 mb-4 flex justify-between items-center">
          <div>
            <h2 class="text-base font-bold text-white uppercase tracking-wider">DGMS Statutory Form-VI Inspection Log</h2>
            <p class="text-xs text-slate-400">Coal Mines Regulations (CMR 2017) Compliant Shift Record</p>
          </div>
          <span class="text-[10px] bg-amber-500/10 border border-amber-500/30 text-amber-400 px-2.5 py-1 rounded font-mono font-bold">DIGITAL SIGNED</span>
        </div>

        <form onsubmit="save(event)" class="space-y-4 text-xs">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-slate-400 text-[11px] mb-1 font-semibold">Colliery Unit</label>
              <select id="sm" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white outline-none focus:border-amber-500"></select>
            </div>
            <div>
              <label class="block text-slate-400 text-[11px] mb-1 font-semibold">Geofence GPS Validation</label>
              <select id="sgps" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-emerald-400 outline-none focus:border-amber-500 font-semibold">
                <option value="inside">Lat: 22.3541 N, Lng: 82.6821 E (Inside Lease Bound)</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label class="block text-slate-400 text-[11px] mb-1 font-semibold">Statutory Officer Name</label>
              <input id="soname" type="text" value="Er. Gaurav Yadav" required class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white outline-none focus:border-amber-500 font-semibold">
            </div>
            <div>
              <label class="block text-slate-400 text-[11px] mb-1 font-semibold">Statutory Capacity</label>
              <select id="sorole" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white outline-none focus:border-amber-500">
                <option value="Safety Officer (Overman)">Safety Officer (Overman / Dy. Mgr)</option>
                <option value="First Class Colliery Manager">First Class Colliery Manager</option>
                <option value="Ventilation Officer">Ventilation Officer (CMR 153)</option>
              </select>
            </div>
            <div>
              <label class="block text-slate-400 text-[11px] mb-1 font-semibold">DGMS Competency Certificate</label>
              <input id="socert" type="text" value="DGMS/CMR/2017/0914" required class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-amber-400 font-mono outline-none focus:border-amber-500 font-bold">
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-slate-400 text-[11px] mb-1 font-semibold">Statutory Regulation Domain</label>
              <select id="scat" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white outline-none focus:border-amber-500">
                <option value="CMR 153: Face Ventilation & Methane Log">CMR 153: Face Ventilation & Methane Log</option>
                <option value="CMR 106: Highwall Bench Stability">CMR 106: Highwall Bench Stability</option>
                <option value="CMR 169: Deep Hole Blasting Vibration">CMR 169: Deep Hole Blasting Vibration</option>
                <option value="CMR 129: Electrical Isolation & Earth Leakage">CMR 129: Electrical Isolation & Earth Leakage</option>
              </select>
            </div>
            <div>
              <label class="block text-slate-400 text-[11px] mb-1 font-semibold">Severity Classification</label>
              <select id="ss" class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white outline-none focus:border-amber-500 font-bold">
                <option value="Normal" class="text-emerald-400 font-bold">Normal - Statutory Compliant</option>
                <option value="Critical" class="text-rose-500 font-bold">Critical - Evacuation Breach</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-slate-400 text-[11px] mb-1 font-semibold">Statutory Observations & Mitigation Orders</label>
            <textarea id="sn" rows="3" required placeholder="Log gas concentration, bench cracks, ventilation velocity or isolation steps..." class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white outline-none focus:border-amber-500 placeholder:text-slate-600 font-sans"></textarea>
          </div>

          <div class="pt-2">
            <button type="submit" class="w-full bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-black font-extrabold p-3 rounded-lg text-sm tracking-wider uppercase shadow-lg">
              Sign, Seal & Commit Inspection Record
            </button>
          </div>
        </form>
      </div>
    </div>
  </main>
"""
