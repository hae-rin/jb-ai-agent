import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ProfileProvider } from './context/ProfileContext'
import { useAdaptive } from './hooks/useAdaptive'
import Layout from './components/Layout'
import Home from './pages/Home'
import CareAgent from './pages/CareAgent'
import Simulation from './pages/Simulation'
import DocReader from './pages/DocReader'
import Products from './pages/Products'
import BucketList from './pages/BucketList'
import VoicePhishing from './pages/VoicePhishing'

function AdaptiveWrapper({ children }: { children: React.ReactNode }) {
  const { isElder } = useAdaptive()
  return <div className={isElder ? 'mode-elder' : ''}>{children}</div>
}

function SubPage({ children }: { children: React.ReactNode }) {
  return <Layout><AdaptiveWrapper>{children}</AdaptiveWrapper></Layout>
}

export default function App() {
  return (
    <ProfileProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/"               element={<Home />} />
          <Route path="/care-agent"     element={<SubPage><CareAgent /></SubPage>} />
          <Route path="/simulation"     element={<SubPage><Simulation /></SubPage>} />
          <Route path="/doc-reader"     element={<SubPage><DocReader /></SubPage>} />
          <Route path="/products"       element={<SubPage><Products /></SubPage>} />
          <Route path="/bucket-list"    element={<SubPage><BucketList /></SubPage>} />
          <Route path="/voice-phishing" element={<SubPage><VoicePhishing /></SubPage>} />
        </Routes>
      </BrowserRouter>
    </ProfileProvider>
  )
}
