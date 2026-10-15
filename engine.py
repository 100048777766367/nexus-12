import os
import sys
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex.omni_intake import OmniIntakeDodecaLobe
from cortex.indra_dodeca_consensus import IndraDodecaConsensusLobe
from cortex.nidana_causal_mind import NidanaCausalMindLobe
from cortex.cosmic_transmute import CosmicTransmuteDodecaLobe

VITAL_CELLS = [
    "cells/linguistic_cell.py",
    "cells/neuron.py",
    "cells/super_xor.py"
]

class Nexus12DodecagonKernel:
    def __init__(self):
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/nexus-12")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.ancestor = f"{self.owner}/nexus-11"
        
        self.lineage = [
            f"{self.owner}/nexus-11", f"{self.owner}/nexus-10",
            f"{self.owner}/nexus-09", f"{self.owner}/nexus-08",
            f"{self.owner}/nexus-07", f"{self.owner}/nexus-06",
            f"{self.owner}/nexus-05", f"{self.owner}/nexus", f"{self.owner}/genome"
        ]

        self.ensure_folders()

        # 4 ĐẠI THÙY DODECAHEDRON F12
        self.omni_lobe = OmniIntakeDodecaLobe(self.owner, self.lineage)
        self.consensus_lobe = IndraDodecaConsensusLobe()
        self.mind_lobe = NidanaCausalMindLobe(num_cells=12)
        self.transmute_lobe = CosmicTransmuteDodecaLobe()

        self.context = {
            "repo_name": self.repo_name,
            "owner": self.owner,
            "ancestor": self.ancestor,
            "peers": self.load_peers(),
            "current_epoch": self.load_epoch()
        }

    def ensure_folders(self):
        for d in ["cells", "cortex", "synapses", "synapses/harvested_memory", "synapses/avatar_proxies"]:
            os.makedirs(d, exist_ok=True)

    def load_peers(self):
        p_file = "synapses/peers.json"
        if os.path.exists(p_file):
            try:
                with open(p_file, "r") as f: return json.load(f).get("trusted_peers", [])
            except Exception: pass
        return [f"{self.owner}/nexus-11", f"{self.owner}/nexus-10", f"{self.owner}/neuron", f"{self.owner}/seed", f"{self.owner}/motor"]

    def load_epoch(self):
        s_file = "synapses/state.json"
        if os.path.exists(s_file):
            try:
                with open(s_file, "r") as f: return json.load(f).get("generation_epoch", 0) + 1
            except Exception: pass
        return 1

    def run(self):
        print("=" * 80)
        print(f"☸️ [NEXUS-12 DODECAGON KERNEL] KHỞI ĐỘNG THẾ HỆ #{self.context['current_epoch']}")
        print(f"👑 Bậc: F12 Thập Nhị Nhân Duyên – Đại Khởi Sinh Vũ Trụ Dodecahedron")
        print("=" * 80)

        # 1. Thùy Cảm Thụ: Hấp thụ Nang F11, Lọc Stateless Token & Vector 12D
        self.omni_lobe.process(self.context, VITAL_CELLS)

        # 2. Thùy Đồng Thuận: Chiếu 12 mặt phẳng Dodecahedron & Kuramoto 12 Pha
        self.consensus_lobe.process(self.context)

        # 3. Thùy Tâm Thức: Quản trị 12 Duyên Khởi, Diệt Đế & Giả lập 12 Tương lai What-If
        self.mind_lobe.process(self.context)

        # 4. Thùy Chấp Hành: La bàn Duyên Khởi, Hộ mệnh 404 & Merkle-DAG 12D CID
        self.transmute_lobe.process(self.context)

        print("=" * 80)
        print(f"✨ [HOÀN TẤT VÒNG ĐỜI F12] Thập Nhị Nhân Duyên đã chuyển hóa đại viên mãn!")
        print("=" * 80)

if __name__ == "__main__":
    node = Nexus12DodecagonKernel()
    node.run()
