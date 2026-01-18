import React, { useState, useEffect, useRef } from 'react';

// ═══════════════════════════════════════════════════════════════════════════════
// BANKING AS A SERVICE - ANIMAÇÃO PEDAGÓGICA INTERATIVA
// Baseado na Consulta Pública BCB 108/2024 e Pesquisa Internacional sobre BaaS
// ═══════════════════════════════════════════════════════════════════════════════

const BaaSAnimation = () => {
  const [currentSection, setCurrentSection] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [selectedModel, setSelectedModel] = useState(null);
  const [showRisks, setShowRisks] = useState(false);
  const [activeParticipant, setActiveParticipant] = useState(null);
  const [flowAnimation, setFlowAnimation] = useState(0);
  const [hoveredService, setHoveredService] = useState(null);
  const intervalRef = useRef(null);

  // Adicionar useCallback para estabilizar as funções
  const { useCallback } = React;

  // Seções principais da apresentação
  const sections = [
    { id: 0, title: 'Introdução', icon: '🏦' },
    { id: 1, title: 'Ecossistema', icon: '🔄' },
    { id: 2, title: 'Modelos de Negócio', icon: '💼' },
    { id: 3, title: 'Serviços BaaS', icon: '⚙️' },
    { id: 4, title: 'Regulação BCB', icon: '📋' },
    { id: 5, title: 'Riscos', icon: '⚠️' },
    { id: 6, title: 'Oportunidades', icon: '🚀' },
    { id: 7, title: 'Cenário Global', icon: '🌍' },
  ];

  // Função estável para alternar participante ativo
  const toggleParticipant = useCallback((participantId) => {
    setActiveParticipant(prev => prev === participantId ? null : participantId);
  }, []);

  // Animação automática do fluxo
  useEffect(() => {
    // Pausar animação quando há seleção ativa (Ecossistema ou Modelos)
    const shouldPause = (currentSection === 1 && activeParticipant) || 
                        (currentSection === 2 && selectedModel);
    
    if (isPlaying && !shouldPause) {
      intervalRef.current = setInterval(() => {
        setFlowAnimation(prev => (prev + 1) % 100);
      }, 100);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [isPlaying, currentSection, activeParticipant, selectedModel]);

  // Auto-play inicial
  useEffect(() => {
    setIsPlaying(true);
  }, []);

  // ═══════════════════════════════════════════════════════════════════════════════
  // SEÇÃO 0: INTRODUÇÃO
  // ═══════════════════════════════════════════════════════════════════════════════
  const IntroSection = () => (
    <div className="relative h-full flex flex-col items-center justify-center p-8">
      {/* Background animado */}
      <div className="absolute inset-0 overflow-hidden">
        <div 
          className="absolute w-96 h-96 rounded-full opacity-10"
          style={{
            background: 'radial-gradient(circle, #0ea5e9 0%, transparent 70%)',
            top: '10%',
            left: '10%',
            transform: `translate(${Math.sin(flowAnimation * 0.05) * 20}px, ${Math.cos(flowAnimation * 0.05) * 20}px)`,
            transition: 'transform 0.5s ease-out'
          }}
        />
        <div 
          className="absolute w-80 h-80 rounded-full opacity-10"
          style={{
            background: 'radial-gradient(circle, #8b5cf6 0%, transparent 70%)',
            bottom: '10%',
            right: '10%',
            transform: `translate(${Math.cos(flowAnimation * 0.03) * 30}px, ${Math.sin(flowAnimation * 0.03) * 30}px)`,
            transition: 'transform 0.5s ease-out'
          }}
        />
      </div>

      {/* Conteúdo principal */}
      <div className="relative z-10 text-center max-w-4xl">
        <div 
          className="inline-block mb-6 px-4 py-2 rounded-full text-sm font-medium tracking-wider"
          style={{
            background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%)',
            border: '1px solid rgba(14, 165, 233, 0.3)',
            color: '#0ea5e9'
          }}
        >
          CONSULTA PÚBLICA BCB Nº 108/2024
        </div>

        <h1 
          className="text-6xl font-bold mb-6 tracking-tight"
          style={{
            background: 'linear-gradient(135deg, #f8fafc 0%, #94a3b8 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontFamily: "'Outfit', sans-serif"
          }}
        >
          Banking as a Service
        </h1>

        <p className="text-xl text-slate-400 mb-12 leading-relaxed max-w-2xl mx-auto">
          A transformação digital dos serviços financeiros através de parcerias 
          entre instituições autorizadas e entidades terceiras
        </p>

        {/* Cards de destaque */}
        <div className="grid grid-cols-3 gap-6 mb-12">
          {[
            { label: 'Instituições', value: 'Financeiras', desc: 'Bancos, IPs, SCDs', color: '#0ea5e9' },
            { label: 'Entidades', value: 'Terceiras', desc: 'Fintechs, Varejistas', color: '#8b5cf6' },
            { label: 'Clientes', value: 'Finais', desc: 'Consumidores, PJs', color: '#10b981' }
          ].map((item, idx) => (
            <div
              key={idx}
              className="p-6 rounded-2xl transition-all duration-500 hover:scale-105 cursor-pointer group"
              style={{
                background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%)',
                border: `1px solid ${item.color}30`,
                boxShadow: `0 0 40px ${item.color}10`
              }}
            >
              <div 
                className="text-4xl font-bold mb-2 transition-transform"
                style={{ color: item.color }}
              >
                {item.value}
              </div>
              <div className="text-slate-400 text-sm uppercase tracking-wider mb-1">{item.label}</div>
              <div className="text-slate-500 text-xs">{item.desc}</div>
            </div>
          ))}
        </div>

        {/* Definição */}
        <div 
          className="p-8 rounded-3xl text-left"
          style={{
            background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%)',
            border: '1px solid rgba(100, 116, 139, 0.2)'
          }}
        >
          <div className="flex items-start gap-4">
            <div 
              className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shrink-0"
              style={{ background: 'linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%)' }}
            >
              💡
            </div>
            <div>
              <h3 className="text-lg font-semibold text-slate-200 mb-2">O que é BaaS?</h3>
              <p className="text-slate-400 leading-relaxed">
                <span className="text-cyan-400 font-medium">Banking as a Service</span> é um modelo onde instituições 
                autorizadas pelo Banco Central disponibilizam sua infraestrutura regulamentada para que 
                entidades terceiras possam oferecer <span className="text-violet-400 font-medium">produtos e serviços financeiros</span> aos 
                seus próprios clientes, mantendo a experiência integrada ao seu ecossistema.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // ═══════════════════════════════════════════════════════════════════════════════
  // SEÇÃO 1: ECOSSISTEMA
  // ═══════════════════════════════════════════════════════════════════════════════
  const EcosystemSection = () => {
    const participants = [
      {
        id: 'bank',
        name: 'Instituição Prestadora',
        subtitle: 'Banco, IP, SCD',
        icon: '🏛️',
        color: '#0ea5e9',
        x: 50,
        y: 20,
        responsibilities: [
          'Licença regulatória',
          'Gestão de balanço',
          'Conformidade PLD/FT',
          'Supervisão de riscos',
          'Reporte ao BCB'
        ]
      },
      {
        id: 'middleware',
        name: 'Middleware',
        subtitle: 'Opcional',
        icon: '🔌',
        color: '#f59e0b',
        x: 50,
        y: 50,
        responsibilities: [
          'Integração técnica',
          'APIs unificadas',
          'Gestão de programa',
          'Suporte operacional'
        ]
      },
      {
        id: 'fintech',
        name: 'Tomador de Serviços',
        subtitle: 'Fintech, Varejo',
        icon: '📱',
        color: '#8b5cf6',
        x: 50,
        y: 80,
        responsibilities: [
          'Tecnologia e UX',
          'Aquisição de clientes',
          'Marketing',
          'Relacionamento'
        ]
      },
      {
        id: 'bcb',
        name: 'Banco Central',
        subtitle: 'Regulador',
        icon: '⚖️',
        color: '#10b981',
        x: 15,
        y: 50,
        responsibilities: [
          'Regulação',
          'Supervisão',
          'Autorização',
          'Fiscalização'
        ]
      },
      {
        id: 'client',
        name: 'Cliente Final',
        subtitle: 'PF ou PJ',
        icon: '👤',
        color: '#ec4899',
        x: 85,
        y: 50,
        responsibilities: [
          'Acesso a serviços',
          'Experiência integrada',
          'Proteção regulatória'
        ]
      }
    ];

    const connections = [
      { from: 'bank', to: 'middleware', label: 'Contrato BaaS' },
      { from: 'middleware', to: 'fintech', label: 'APIs' },
      { from: 'bank', to: 'fintech', label: 'Supervisão' },
      { from: 'bcb', to: 'bank', label: 'Regulação' },
      { from: 'fintech', to: 'client', label: 'Serviços' },
      { from: 'bank', to: 'client', label: 'Responsabilidade' }
    ];

    const getParticipantPosition = (id) => {
      const p = participants.find(p => p.id === id);
      return { x: p.x, y: p.y };
    };

    return (
      <div className="h-full flex flex-col p-8 overflow-auto">
        <h2 className="text-2xl font-bold text-slate-200 mb-2">Ecossistema BaaS</h2>
        <p className="text-slate-400 mb-6">Clique em cada participante para explorar suas responsabilidades</p>

        {/* Diagrama do ecossistema */}
        <div className="relative h-[400px] rounded-3xl overflow-hidden mb-6"
          style={{
            background: 'linear-gradient(145deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.5) 100%)',
            border: '1px solid rgba(100, 116, 139, 0.2)'
          }}
        >
          {/* SVG para conexões */}
          <svg className="absolute inset-0 w-full h-full" style={{ zIndex: 1 }}>
            <defs>
              <linearGradient id="flowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.2" />
                <stop offset={`${flowAnimation}%`} stopColor="#0ea5e9" stopOpacity="1" />
                <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.2" />
              </linearGradient>
            </defs>
            {connections.map((conn, idx) => {
              const from = getParticipantPosition(conn.from);
              const to = getParticipantPosition(conn.to);
              return (
                <g key={idx}>
                  <line
                    x1={`${from.x}%`}
                    y1={`${from.y}%`}
                    x2={`${to.x}%`}
                    y2={`${to.y}%`}
                    stroke="rgba(100, 116, 139, 0.3)"
                    strokeWidth="2"
                    strokeDasharray="5,5"
                  />
                  {!activeParticipant && (
                    <circle
                      cx={`${from.x + (to.x - from.x) * (flowAnimation / 100)}%`}
                      cy={`${from.y + (to.y - from.y) * (flowAnimation / 100)}%`}
                      r="4"
                      fill="#0ea5e9"
                      opacity="0.8"
                    />
                  )}
                </g>
              );
            })}
          </svg>

          {/* Participantes */}
          {participants.map((p) => (
            <div
              key={p.id}
              className={`absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-all duration-300 ${
                activeParticipant === p.id ? 'scale-110 z-20' : 'z-10 hover:scale-105'
              }`}
              style={{ left: `${p.x}%`, top: `${p.y}%` }}
              onClick={(e) => {
                e.stopPropagation();
                setActiveParticipant(p.id);
              }}
            >
              <div
                className="w-24 h-24 rounded-2xl flex flex-col items-center justify-center transition-all duration-300"
                style={{
                  background: `linear-gradient(145deg, ${p.color}20 0%, ${p.color}10 100%)`,
                  border: `2px solid ${activeParticipant === p.id ? p.color : p.color + '50'}`,
                  boxShadow: activeParticipant === p.id ? `0 0 30px ${p.color}40` : 'none'
                }}
              >
                <span className="text-3xl mb-1">{p.icon}</span>
                <span className="text-xs text-slate-300 font-medium text-center px-2">{p.name}</span>
              </div>
              <div className="text-center mt-2">
                <span className="text-xs text-slate-500">{p.subtitle}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Painel de detalhes - AGORA ABAIXO DO DIAGRAMA */}
        <div 
          className="p-6 rounded-2xl min-h-[200px]"
          style={{ 
            background: 'rgba(30, 41, 59, 0.8)',
            border: '1px solid rgba(100, 116, 139, 0.2)'
          }}
        >
          {activeParticipant ? (
            (() => {
              const p = participants.find(p => p.id === activeParticipant);
              return (
                <div className="animate-fadeIn">
                  <div className="flex items-center gap-4 mb-6">
                    <div 
                      className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl"
                      style={{ background: `${p.color}20`, border: `2px solid ${p.color}` }}
                    >
                      {p.icon}
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-slate-200 mb-1">{p.name}</h3>
                      <p className="text-sm text-slate-500">{p.subtitle}</p>
                    </div>
                  </div>
                  
                  <h4 className="text-xs uppercase tracking-wider text-slate-500 mb-3">Responsabilidades</h4>
                  <div className="grid grid-cols-2 gap-2">
                    {p.responsibilities.map((r, idx) => (
                      <div 
                        key={idx}
                        className="flex items-center gap-2 text-slate-300 text-sm p-3 rounded-lg transition-colors hover:bg-slate-800/50"
                      >
                        <span 
                          className="w-2 h-2 rounded-full flex-shrink-0"
                          style={{ background: p.color }}
                        />
                        {r}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })()
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center py-8">
              <div className="text-4xl mb-4 opacity-50">👆</div>
              <p className="text-slate-500">Selecione um participante para ver detalhes</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  // ═══════════════════════════════════════════════════════════════════════════════
  // SEÇÃO 2: MODELOS DE NEGÓCIO
  // ═══════════════════════════════════════════════════════════════════════════════
  const BusinessModelsSection = () => {
    const models = [
      {
        id: 'direct',
        name: 'Parceria Direta',
        desc: 'Integração direta entre instituição e tomador',
        icon: '🤝',
        color: '#0ea5e9',
        pros: ['Maior controle', 'Sem intermediários', 'Flexibilidade'],
        cons: ['Maior complexidade técnica', 'Investimento em compliance', 'Time to market maior'],
        flow: ['Instituição', '', 'Tomador', '', 'Cliente']
      },
      {
        id: 'middleware',
        name: 'Via Middleware',
        desc: 'Plataforma intermediária facilita a integração',
        icon: '🔗',
        color: '#8b5cf6',
        pros: ['Integração simplificada', 'Time to market menor', 'Suporte técnico'],
        cons: ['Dependência do intermediário', 'Menor flexibilidade', 'Risco adicional'],
        flow: ['Instituição', '', 'Middleware', '', 'Tomador', '', 'Cliente']
      },
      {
        id: 'api-native',
        name: 'Banco Nativo API',
        desc: 'Instituições construídas para BaaS desde o início',
        icon: '⚡',
        color: '#10b981',
        pros: ['Tecnologia moderna', 'Alta performance', 'Escalabilidade'],
        cons: ['Mercado ainda em desenvolvimento', 'Poucos players', 'Custo elevado'],
        flow: ['Banco API', '', 'Tomador', '', 'Cliente']
      }
    ];

    return (
      <div className="h-full p-8 overflow-auto">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-200 mb-2">Modelos de Negócio BaaS</h2>
          <p className="text-slate-400 mb-8">Selecione um modelo para visualizar o fluxo operacional</p>

          <div className="grid grid-cols-3 gap-6 mb-8">
            {models.map((model) => (
              <div
                key={model.id}
                className={`p-6 rounded-2xl cursor-pointer transition-all duration-300 ${
                  selectedModel === model.id ? 'scale-105' : 'hover:scale-102'
                }`}
                style={{
                  background: selectedModel === model.id 
                    ? `linear-gradient(145deg, ${model.color}20 0%, ${model.color}10 100%)`
                    : 'linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%)',
                  border: `2px solid ${selectedModel === model.id ? model.color : 'rgba(100, 116, 139, 0.2)'}`,
                  boxShadow: selectedModel === model.id ? `0 0 40px ${model.color}20` : 'none'
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedModel(model.id);
                }}
              >
                <div className="text-4xl mb-4">{model.icon}</div>
                <h3 className="text-lg font-bold text-slate-200 mb-2">{model.name}</h3>
                <p className="text-sm text-slate-400">{model.desc}</p>
              </div>
            ))}
          </div>

          {/* Detalhes do modelo selecionado */}
          {selectedModel && (
            <div 
              className="p-8 rounded-3xl animate-fadeIn"
              style={{
                background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%)',
                border: '1px solid rgba(100, 116, 139, 0.2)'
              }}
            >
              {(() => {
                const model = models.find(m => m.id === selectedModel);
                if (!model) return null;
                
                return (
                  <>
                    {/* Fluxo visual */}
                    <div className="mb-8">
                      <h4 className="text-sm uppercase tracking-wider text-slate-500 mb-4">Fluxo Operacional</h4>
                      <div className="flex items-center justify-center gap-2">
                        {model.flow.map((step, idx) => (
                          step ? (
                            <div
                              key={idx}
                              className="px-6 py-3 rounded-xl font-medium text-slate-200"
                              style={{
                                background: `${model.color}20`,
                                border: `1px solid ${model.color}50`
                              }}
                            >
                              {step}
                            </div>
                          ) : (
                            <div key={idx} className="flex items-center">
                              <svg width="40" height="20" className="text-slate-500">
                                <path 
                                  d="M0 10 L30 10 M25 5 L30 10 L25 15" 
                                  fill="none" 
                                  stroke={model.color}
                                  strokeWidth="2"
                                  opacity="0.5"
                                />
                                {/* Ponto animado */}
                                <circle
                                  cx={flowAnimation % 30}
                                  cy="10"
                                  r="3"
                                  fill={model.color}
                                />
                              </svg>
                            </div>
                          )
                        ))}
                      </div>
                    </div>

                    {/* Prós e Contras */}
                    <div className="grid grid-cols-2 gap-8">
                      <div>
                        <h4 className="flex items-center gap-2 text-sm uppercase tracking-wider text-emerald-400 mb-4">
                          <span>✓</span> Vantagens
                        </h4>
                        <ul className="space-y-2">
                          {model.pros.map((pro, idx) => (
                            <li 
                              key={idx}
                              className="flex items-center gap-3 text-slate-300 text-sm p-3 rounded-lg bg-emerald-500/10"
                            >
                              <span className="w-2 h-2 rounded-full bg-emerald-400" />
                              {pro}
                            </li>
                          ))}
                        </ul>
                      </div>
                      <div>
                        <h4 className="flex items-center gap-2 text-sm uppercase tracking-wider text-rose-400 mb-4">
                          <span>✗</span> Desafios
                        </h4>
                        <ul className="space-y-2">
                          {model.cons.map((con, idx) => (
                            <li 
                              key={idx}
                              className="flex items-center gap-3 text-slate-300 text-sm p-3 rounded-lg bg-rose-500/10"
                            >
                              <span className="w-2 h-2 rounded-full bg-rose-400" />
                              {con}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </>
                );
              })()}
            </div>
          )}
        </div>
      </div>
    );
  };

  // ═══════════════════════════════════════════════════════════════════════════════
  // SEÇÃO 3: SERVIÇOS BaaS
  // ═══════════════════════════════════════════════════════════════════════════════
  const ServicesSection = () => {
    const services = [
      {
        id: 'account',
        name: 'Contas de Pagamento',
        icon: '💳',
        color: '#0ea5e9',
        desc: 'Abertura e manutenção de contas para clientes',
        details: ['Conta corrente', 'Conta poupança', 'Conta de pagamento pré-paga'],
        status: 'Previsto na minuta'
      },
      {
        id: 'pix',
        name: 'Pix',
        icon: '⚡',
        color: '#10b981',
        desc: 'Serviços de pagamento instantâneo',
        details: ['Pix QR Code', 'Pix Copia e Cola', 'Pix Saque', 'Pix Troco'],
        status: 'Previsto na minuta'
      },
      {
        id: 'cards',
        name: 'Emissão de Cartões',
        icon: '💎',
        color: '#8b5cf6',
        desc: 'Cartões de débito, crédito e pré-pagos',
        details: ['Cartão físico', 'Cartão virtual', 'Tokenização'],
        status: 'Previsto na minuta'
      },
      {
        id: 'credit',
        name: 'Operações de Crédito',
        icon: '📈',
        color: '#f59e0b',
        desc: 'Oferta e contratação de empréstimos',
        details: ['Crédito pessoal', 'Financiamentos', 'Antecipação de recebíveis'],
        status: 'Em discussão'
      },
      {
        id: 'acquiring',
        name: 'Credenciamento',
        icon: '🏪',
        color: '#ec4899',
        desc: 'Aceitação de instrumentos de pagamento',
        details: ['Credenciamento de estabelecimentos', 'Subcredenciamento regulado'],
        status: 'Proposta de inclusão'
      },
      {
        id: 'itp',
        name: 'Iniciação de Pagamento',
        icon: '🔄',
        color: '#06b6d4',
        desc: 'Início de transações via Open Finance',
        details: ['ITP (Iniciador de Transação de Pagamento)', 'Open Banking'],
        status: 'Em avaliação'
      },
      {
        id: 'efx',
        name: 'eFX - Câmbio',
        icon: '🌎',
        color: '#14b8a6',
        desc: 'Pagamentos e transferências internacionais',
        details: ['Remessas internacionais', 'Pagamentos cross-border'],
        status: 'Em avaliação'
      },
      {
        id: 'investment',
        name: 'Investimentos',
        icon: '📊',
        color: '#6366f1',
        desc: 'Distribuição de produtos de investimento',
        details: ['CDB', 'Fundos', 'Previdência'],
        status: 'Possível expansão'
      }
    ];

    return (
      <div className="h-full p-8 overflow-auto">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-200 mb-2">Serviços no Escopo do BaaS</h2>
          <p className="text-slate-400 mb-8">Conforme proposta da Consulta Pública BCB 108/2024</p>

          <div className="grid grid-cols-4 gap-4">
            {services.map((service) => (
            <div
              key={service.id}
              className="relative rounded-2xl cursor-pointer transition-all duration-300 group"
              style={{
                background: hoveredService === service.id 
                  ? `linear-gradient(145deg, ${service.color}20 0%, ${service.color}10 100%)`
                  : 'linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%)',
                border: `1px solid ${hoveredService === service.id ? service.color : 'rgba(100, 116, 139, 0.2)'}`,
                boxShadow: hoveredService === service.id ? `0 0 30px ${service.color}20` : 'none',
                height: '280px',
                display: 'flex',
                flexDirection: 'column',
                overflow: 'hidden'
              }}
              onMouseEnter={() => setHoveredService(service.id)}
              onMouseLeave={() => setHoveredService(null)}
            >
              {/* Conteúdo fixo no topo */}
              <div className="p-5 flex-shrink-0">
                {/* Status badge */}
                <div 
                  className="absolute -top-2 -right-2 px-2 py-1 rounded-full text-xs font-medium z-10"
                  style={{
                    background: service.status.includes('Previsto') ? '#10b98130' : 
                              service.status.includes('avaliação') ? '#f59e0b30' : '#64748b30',
                    color: service.status.includes('Previsto') ? '#10b981' : 
                          service.status.includes('avaliação') ? '#f59e0b' : '#94a3b8',
                    border: `1px solid ${service.status.includes('Previsto') ? '#10b98150' : 
                            service.status.includes('avaliação') ? '#f59e0b50' : '#64748b50'}`
                  }}
                >
                  {service.status.includes('Previsto') ? '✓' : service.status.includes('avaliação') ? '?' : '○'}
                </div>

                <div className="text-3xl mb-3">
                  {service.icon}
                </div>
                <h3 className="text-base font-semibold text-slate-200 mb-1 leading-tight">{service.name}</h3>
                <p className="text-xs text-slate-500 leading-relaxed">{service.desc}</p>
              </div>

              {/* Detalhes expandidos - posição absoluta para não afetar layout */}
              <div 
                className="absolute bottom-0 left-0 right-0 px-5 pb-5 pt-3 bg-gradient-to-t from-slate-900/95 to-transparent"
                style={{
                  opacity: hoveredService === service.id ? 1 : 0,
                  transform: hoveredService === service.id ? 'translateY(0)' : 'translateY(10px)',
                  transition: 'opacity 0.3s ease, transform 0.3s ease',
                  pointerEvents: hoveredService === service.id ? 'auto' : 'none'
                }}
              >
                <div className="border-t border-slate-700/50 pt-3">
                  <div className="text-xs text-slate-400 mb-2 font-medium">Inclui:</div>
                  <ul className="space-y-1.5">
                    {service.details.map((detail, idx) => (
                      <li 
                        key={idx}
                        className="text-xs text-slate-300 flex items-start gap-2"
                      >
                        <span 
                          className="w-1.5 h-1.5 rounded-full mt-1 flex-shrink-0"
                          style={{ background: service.color }}
                        />
                        <span className="leading-tight">{detail}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
            ))}
          </div>

          {/* Legenda de status */}
          <div 
            className="mt-8 p-6 rounded-2xl flex items-center justify-center gap-8"
            style={{
              background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%)',
              border: '1px solid rgba(100, 116, 139, 0.1)'
            }}
          >
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-emerald-500" />
              <span className="text-sm text-slate-400">Previsto na minuta</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-amber-500" />
              <span className="text-sm text-slate-400">Em avaliação pelo BCB</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-3 rounded-full bg-slate-500" />
              <span className="text-sm text-slate-400">Possível expansão futura</span>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // ═══════════════════════════════════════════════════════════════════════════════
  // SEÇÃO 4: REGULAÇÃO BCB
  // ═══════════════════════════════════════════════════════════════════════════════
  const RegulationSection = () => {
    const principles = [
      { icon: '🔍', title: 'Transparência', desc: 'Clareza nas informações ao cliente sobre quem presta o serviço' },
      { icon: '⚖️', title: 'Conduta', desc: 'Normas de comportamento para proteção do consumidor' },
      { icon: '🛡️', title: 'PLD/FT', desc: 'Prevenção à lavagem de dinheiro e financiamento do terrorismo' },
      { icon: '🔒', title: 'Controles Internos', desc: 'Mecanismos de acompanhamento e gestão de riscos' },
      { icon: '📋', title: 'Responsabilização', desc: 'Definição clara de responsabilidades das partes' },
      { icon: '📊', title: 'Prudencial', desc: 'Requerimentos de capital e patrimônio líquido em avaliação' }
    ];

    const timeline = [
      { date: 'Out/2024', event: 'Publicação CP 108/2024', status: 'done' },
      { date: 'Jan/2025', event: 'Prazo original para contribuições', status: 'done' },
      { date: 'Fev/2025', event: 'Prazo prorrogado (CP 115/2025)', status: 'current' },
      { date: '2025', event: 'Análise das contribuições', status: 'pending' },
      { date: '2025', event: 'Resolução Conjunta CMN/BCB', status: 'pending' },
      { date: 'TBD', event: 'Prazo para adequação', status: 'pending' }
    ];

    return (
      <div className="h-full p-8 overflow-auto">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-2 gap-8">
            {/* Princípios */}
            <div>
              <h2 className="text-2xl font-bold text-slate-200 mb-2">Princípios da Regulação</h2>
              <p className="text-slate-400 mb-6">Base normativa proposta pelo BCB</p>

              <div className="space-y-4">
                {principles.map((p, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-xl transition-all duration-300 hover:scale-102 group"
                    style={{
                      background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%)',
                      border: '1px solid rgba(100, 116, 139, 0.2)'
                    }}
                  >
                    <div className="flex items-start gap-4">
                      <div className="text-2xl group-hover:scale-110 transition-transform">
                        {p.icon}
                      </div>
                      <div>
                        <h3 className="font-semibold text-slate-200">{p.title}</h3>
                        <p className="text-sm text-slate-400">{p.desc}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Timeline */}
            <div>
              <h2 className="text-2xl font-bold text-slate-200 mb-2">Cronograma Regulatório</h2>
              <p className="text-slate-400 mb-6">Processo de consulta pública</p>

              <div 
                className="p-6 rounded-2xl"
                style={{
                  background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%)',
                  border: '1px solid rgba(100, 116, 139, 0.2)'
                }}
              >
                <div className="relative">
                  {/* Linha vertical */}
                  <div 
                    className="absolute left-4 top-0 bottom-0 w-0.5"
                    style={{ background: 'linear-gradient(to bottom, #0ea5e9, #8b5cf6)' }}
                  />

                  {timeline.map((item, idx) => (
                    <div key={idx} className="relative pl-12 pb-6 last:pb-0">
                      {/* Ponto na timeline */}
                      <div 
                        className={`absolute left-2 w-5 h-5 rounded-full border-2 transition-all ${
                          item.status === 'done' ? 'bg-emerald-500 border-emerald-400' :
                          item.status === 'current' ? 'bg-cyan-500 border-cyan-400 animate-pulse' :
                          'bg-slate-700 border-slate-600'
                        }`}
                      />
                      
                      <div className="flex items-start justify-between">
                        <div>
                          <div 
                            className={`text-sm font-medium ${
                              item.status === 'current' ? 'text-cyan-400' : 
                              item.status === 'done' ? 'text-emerald-400' : 'text-slate-500'
                            }`}
                          >
                            {item.date}
                          </div>
                          <div className="text-slate-300">{item.event}</div>
                        </div>
                        {item.status === 'current' && (
                          <span 
                            className="px-2 py-1 rounded-full text-xs font-medium"
                            style={{
                              background: '#0ea5e930',
                              color: '#0ea5e9',
                              border: '1px solid #0ea5e950'
                            }}
                          >
                            ATUAL
                          </span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Temas em discussão */}
              <div 
                className="mt-6 p-6 rounded-2xl"
                style={{
                  background: 'linear-gradient(145deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%)',
                  border: '1px solid rgba(245, 158, 11, 0.3)'
                }}
              >
                <h4 className="flex items-center gap-2 text-amber-400 font-semibold mb-3">
                  <span>💬</span> Temas em Discussão
                </h4>
                <ul className="space-y-2 text-sm text-slate-300">
                  <li>• Subcredenciamento exclusivo via BaaS</li>
                  <li>• Inclusão de ITP e eFX no escopo</li>
                  <li>• Relação com correspondentes no país</li>
                  <li>• Requerimentos prudenciais adicionais</li>
                  <li>• Prazos de adequação dos contratos</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // ═══════════════════════════════════════════════════════════════════════════════
  // SEÇÃO 5: RISCOS
  // ═══════════════════════════════════════════════════════════════════════════════
  const RisksSection = () => {
    const riskCategories = [
      {
        category: 'Regulatórios',
        color: '#ef4444',
        icon: '⚖️',
        risks: [
          { name: 'Conformidade PLD/FT', severity: 5, desc: 'Falhas em KYC e monitoramento de transações' },
          { name: 'True Lender', severity: 4, desc: 'Questionamento sobre quem é o verdadeiro credor' },
          { name: 'Gestão de Terceiros', severity: 4, desc: 'Supervisão inadequada de parceiros' },
          { name: 'Fiscalização', severity: 3, desc: 'Ações de enforcement e multas' }
        ]
      },
      {
        category: 'Operacionais',
        color: '#f59e0b',
        icon: '⚙️',
        risks: [
          { name: 'Reconciliação', severity: 4, desc: 'Complexidade em contas FBO/omnibus' },
          { name: 'Dependência Tecnológica', severity: 4, desc: 'Falhas em middleware ou APIs' },
          { name: 'Continuidade', severity: 3, desc: 'Risco de falência de parceiros (caso Synapse)' },
          { name: 'Segurança Cibernética', severity: 5, desc: 'Ataques e vazamento de dados' }
        ]
      },
      {
        category: 'Reputacionais',
        color: '#8b5cf6',
        icon: '🏢',
        risks: [
          { name: 'Imagem Institucional', severity: 3, desc: 'Associação com práticas inadequadas' },
          { name: 'Confiança do Cliente', severity: 4, desc: 'Experiência ruim reflete em todas as partes' },
          { name: 'Transparência', severity: 3, desc: 'Confusão sobre responsabilidades' }
        ]
      },
      {
        category: 'Econômicos',
        color: '#06b6d4',
        icon: '📉',
        risks: [
          { name: 'Modelo de Receita', severity: 4, desc: 'Dependência de intercâmbio ou VC' },
          { name: 'Custos de Compliance', severity: 4, desc: 'Aumento de investimentos regulatórios' },
          { name: 'Churn de Parceiros', severity: 3, desc: 'Fintechs que falham ou migram' }
        ]
      }
    ];

    return (
      <div className="h-full p-8 overflow-auto">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-200 mb-2">Mapeamento de Riscos</h2>
          <p className="text-slate-400 mb-8">Principais riscos identificados no modelo BaaS</p>

          <div className="grid grid-cols-2 gap-6 mb-6">
            {riskCategories.map((cat) => (
              <div
                key={cat.category}
                className="p-6 rounded-2xl"
                style={{
                  background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%)',
                  border: `1px solid ${cat.color}30`
                }}
              >
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-2xl">{cat.icon}</span>
                  <h3 
                    className="text-lg font-semibold"
                    style={{ color: cat.color }}
                  >
                    Riscos {cat.category}
                  </h3>
                </div>

                <div className="space-y-3">
                  {cat.risks.map((risk, idx) => (
                    <div key={idx} className="group">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm text-slate-300 font-medium">{risk.name}</span>
                        <div className="flex gap-1">
                          {[1, 2, 3, 4, 5].map((level) => (
                            <div
                              key={level}
                              className="w-2 h-2 rounded-full transition-all"
                              style={{
                                background: level <= risk.severity ? cat.color : 'rgba(100, 116, 139, 0.3)',
                                opacity: level <= risk.severity ? 1 : 0.3
                              }}
                            />
                          ))}
                        </div>
                      </div>
                      <p className="text-xs text-slate-500 group-hover:text-slate-400 transition-colors">
                        {risk.desc}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Case Study: Synapse */}
          <div 
            className="p-6 rounded-2xl"
            style={{
              background: 'linear-gradient(145deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%)',
              border: '1px solid rgba(239, 68, 68, 0.3)'
            }}
          >
            <h4 className="flex items-center gap-2 text-rose-400 font-semibold mb-3">
              <span>⚠️</span> Caso de Estudo: Synapse (2024)
            </h4>
            <p className="text-slate-300 text-sm leading-relaxed">
              A falência do middleware Synapse nos EUA deixou centenas de milhares de clientes sem acesso aos seus fundos, 
              evidenciando os riscos de modelos com múltiplos intermediários. O caso destacou problemas críticos de 
              reconciliação de contas FBO, supervisão inadequada pelos bancos parceiros e a complexidade de resolver 
              disputas quando há múltiplas camadas entre o cliente e a instituição detentora dos fundos.
            </p>
          </div>
        </div>
      </div>
    );
  };

  // ═══════════════════════════════════════════════════════════════════════════════
  // SEÇÃO 6: OPORTUNIDADES
  // ═══════════════════════════════════════════════════════════════════════════════
  const OpportunitiesSection = () => {
    const opportunities = [
      {
        icon: '🚀',
        title: 'Inclusão Financeira',
        desc: 'Ampliação do acesso a serviços financeiros para populações desbancarizadas através de canais não tradicionais',
        color: '#10b981',
        metrics: ['40M+ brasileiros desbancarizados', 'Varejo como canal de acesso']
      },
      {
        icon: '💡',
        title: 'Inovação',
        desc: 'Desenvolvimento de novos produtos e experiências financeiras integradas a jornadas de consumo',
        color: '#8b5cf6',
        metrics: ['Embedded Finance', 'Finanças contextuais']
      },
      {
        icon: '📈',
        title: 'Novos Mercados',
        desc: 'Acesso a segmentos de clientes anteriormente inviáveis economicamente para instituições tradicionais',
        color: '#0ea5e9',
        metrics: ['Long tail de clientes', 'Nichos especializados']
      },
      {
        icon: '💰',
        title: 'Diversificação de Receita',
        desc: 'Para bancos: nova fonte de depósitos e receitas. Para fintechs: monetização de base de clientes',
        color: '#f59e0b',
        metrics: ['Receita de intercâmbio', 'Float de depósitos']
      },
      {
        icon: '⚡',
        title: 'Eficiência Operacional',
        desc: 'Otimização de custos através de especialização e economia de escala em cada elo da cadeia',
        color: '#ec4899',
        metrics: ['APIs padronizadas', 'Processos automatizados']
      },
      {
        icon: '🤝',
        title: 'Competitividade',
        desc: 'Democratização do acesso à infraestrutura bancária, permitindo que novos entrantes compitam',
        color: '#06b6d4',
        metrics: ['Menor barreira de entrada', 'Time to market reduzido']
      }
    ];

    return (
      <div className="h-full p-8 overflow-auto">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-200 mb-2">Oportunidades do BaaS</h2>
          <p className="text-slate-400 mb-8">Benefícios para o sistema financeiro e a sociedade</p>

          <div className="grid grid-cols-3 gap-6">
            {opportunities.map((opp, idx) => (
              <div
                key={idx}
                className="p-6 rounded-2xl transition-all duration-500 hover:scale-105 group cursor-pointer"
                style={{
                  background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%)',
                  border: `1px solid ${opp.color}30`,
                  boxShadow: `0 0 0 ${opp.color}00`
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.boxShadow = `0 0 40px ${opp.color}20`;
                  e.currentTarget.style.borderColor = opp.color;
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.boxShadow = `0 0 0 ${opp.color}00`;
                  e.currentTarget.style.borderColor = `${opp.color}30`;
                }}
              >
                <div 
                  className="w-14 h-14 rounded-xl flex items-center justify-center text-3xl mb-4 group-hover:scale-110 transition-transform"
                  style={{ background: `${opp.color}20` }}
                >
                  {opp.icon}
                </div>
                <h3 className="text-lg font-semibold text-slate-200 mb-2">{opp.title}</h3>
                <p className="text-sm text-slate-400 mb-4 leading-relaxed">{opp.desc}</p>
                
                <div className="space-y-2">
                  {opp.metrics.map((metric, mIdx) => (
                    <div 
                      key={mIdx}
                      className="flex items-center gap-2 text-xs"
                      style={{ color: opp.color }}
                    >
                      <span className="w-1.5 h-1.5 rounded-full" style={{ background: opp.color }} />
                      {metric}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Embedded Finance Highlight */}
          <div 
            className="mt-8 p-8 rounded-3xl relative overflow-hidden"
            style={{
              background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)',
              border: '1px solid rgba(14, 165, 233, 0.3)'
            }}
          >
            {/* Decorative elements */}
            <div 
              className="absolute -right-20 -top-20 w-60 h-60 rounded-full opacity-20"
              style={{
                background: 'radial-gradient(circle, #8b5cf6 0%, transparent 70%)',
              }}
            />
            
            <div className="relative z-10">
              <h3 className="text-xl font-bold text-slate-200 mb-4">
                🔮 Finanças Embutidas (Embedded Finance)
              </h3>
              <p className="text-slate-300 leading-relaxed mb-4">
                O futuro do BaaS está intrinsecamente ligado ao conceito de <span className="text-cyan-400 font-medium">Embedded Finance</span>, 
                onde serviços financeiros são integrados de forma invisível em plataformas não-financeiras. 
                Varejistas, marketplaces, plataformas de software e até redes sociais podem oferecer 
                conta, pagamentos, crédito e seguros sem que o usuário precise sair de sua jornada principal.
              </p>
              <div className="flex gap-4">
                {['E-commerce', 'Mobilidade', 'SaaS B2B', 'Gig Economy'].map((sector, idx) => (
                  <span 
                    key={idx}
                    className="px-3 py-1.5 rounded-full text-sm font-medium"
                    style={{
                      background: 'rgba(14, 165, 233, 0.2)',
                      color: '#0ea5e9',
                      border: '1px solid rgba(14, 165, 233, 0.3)'
                    }}
                  >
                    {sector}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // ═══════════════════════════════════════════════════════════════════════════════
  // SEÇÃO 7: CENÁRIO GLOBAL
  // ═══════════════════════════════════════════════════════════════════════════════
  const GlobalSection = () => {
    const regions = [
      {
        name: 'Estados Unidos',
        flag: '🇺🇸',
        color: '#3b82f6',
        highlight: 'Durbin Amendment',
        desc: 'Mercado impulsionado pela isenção de bancos <$10B dos limites de intercâmbio. Escrutínio regulatório intenso.',
        cases: ['Synapse (falência)', 'Evolve Bank', 'Blue Ridge Bank']
      },
      {
        name: 'Reino Unido / UE',
        flag: '🇬🇧🇪🇺',
        color: '#8b5cf6',
        highlight: 'Licenças Alternativas',
        desc: 'E-money e Payment Institutions reduzem dependência de bancos. Intercâmbio regulado em níveis baixos.',
        cases: ['Railsr', 'Griffin', 'Solaris']
      },
      {
        name: 'América Latina',
        flag: '🌎',
        color: '#10b981',
        highlight: 'Inclusão Financeira',
        desc: 'Oportunidade greenfield. Brasil lidera com Pix e Open Finance. Regulação em evolução.',
        cases: ['Dock', 'Pomelo', 'QI Tech']
      },
      {
        name: 'Ásia-Pacífico',
        flag: '🌏',
        color: '#f59e0b',
        highlight: 'Super Apps',
        desc: 'Alta penetração de e-wallets. Incumbentes inovadores. Mercados diversos.',
        cases: ['Nium', 'Airwallex', 'Standard Chartered']
      }
    ];

    return (
      <div className="h-full p-8 overflow-auto">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold text-slate-200 mb-2">Cenário Global do BaaS</h2>
          <p className="text-slate-400 mb-8">Comparativo de modelos e regulação por região</p>

          <div className="grid grid-cols-2 gap-6 mb-8">
            {regions.map((region) => (
              <div
                key={region.name}
                className="p-6 rounded-2xl transition-all duration-300 hover:scale-102"
                style={{
                  background: 'linear-gradient(145deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%)',
                  border: `1px solid ${region.color}30`
                }}
              >
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-3xl">{region.flag}</span>
                  <div>
                    <h3 className="text-lg font-semibold text-slate-200">{region.name}</h3>
                    <span 
                      className="text-xs font-medium px-2 py-0.5 rounded-full"
                      style={{ background: `${region.color}30`, color: region.color }}
                    >
                      {region.highlight}
                    </span>
                  </div>
                </div>
                <p className="text-sm text-slate-400 mb-4 leading-relaxed">{region.desc}</p>
                <div className="flex flex-wrap gap-2">
                  {region.cases.map((c, idx) => (
                    <span 
                      key={idx}
                      className="text-xs px-2 py-1 rounded-lg bg-slate-800/50 text-slate-400"
                    >
                      {c}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Brasil Highlight */}
          <div 
            className="p-8 rounded-3xl"
            style={{
              background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%)',
              border: '1px solid rgba(16, 185, 129, 0.3)'
            }}
          >
            <div className="flex items-start gap-6">
              <div className="text-6xl">🇧🇷</div>
              <div className="flex-1">
                <h3 className="text-xl font-bold text-slate-200 mb-3">Brasil: Pioneiro em Infraestrutura</h3>
                <p className="text-slate-300 leading-relaxed mb-4">
                  O Brasil possui uma das infraestruturas de pagamentos mais avançadas do mundo. 
                  O <span className="text-emerald-400 font-medium">Pix</span> revolucionou os pagamentos instantâneos, 
                  o <span className="text-cyan-400 font-medium">Open Finance</span> está em expansão, e agora o 
                  <span className="text-violet-400 font-medium"> Drex</span> promete trazer a tokenização ao mainstream. 
                  A regulação do BaaS posiciona o país na vanguarda global.
                </p>
                <div className="grid grid-cols-4 gap-4">
                  {[
                    { label: 'Pix', value: '150M+', desc: 'usuários' },
                    { label: 'Open Finance', value: '45M+', desc: 'consentimentos' },
                    { label: 'Fintechs', value: '1.500+', desc: 'ativas' },
                    { label: 'Drex', value: '2025', desc: 'lançamento' }
                  ].map((stat, idx) => (
                    <div key={idx} className="text-center">
                      <div className="text-2xl font-bold text-emerald-400">{stat.value}</div>
                      <div className="text-sm text-slate-400">{stat.label}</div>
                      <div className="text-xs text-slate-500">{stat.desc}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // ═══════════════════════════════════════════════════════════════════════════════
  // RENDER PRINCIPAL
  // ═══════════════════════════════════════════════════════════════════════════════
  const renderSection = () => {
    switch (currentSection) {
      case 0: return <IntroSection />;
      case 1: return <EcosystemSection />;
      case 2: return <BusinessModelsSection />;
      case 3: return <ServicesSection />;
      case 4: return <RegulationSection />;
      case 5: return <RisksSection />;
      case 6: return <OpportunitiesSection />;
      case 7: return <GlobalSection />;
      default: return <IntroSection />;
    }
  };

  return (
    <div 
      className="w-full h-screen flex flex-col overflow-hidden"
      style={{
        background: 'linear-gradient(145deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)',
        fontFamily: "'Outfit', 'Inter', system-ui, sans-serif"
      }}
    >
      {/* Header com navegação */}
      <header 
        className="flex items-center justify-between px-6 py-4 border-b"
        style={{ 
          background: 'rgba(15, 23, 42, 0.9)',
          borderColor: 'rgba(100, 116, 139, 0.2)',
          backdropFilter: 'blur(20px)'
        }}
      >
        <div className="flex items-center gap-4">
          <div 
            className="w-10 h-10 rounded-xl flex items-center justify-center"
            style={{ 
              background: 'linear-gradient(135deg, #0ea5e9 0%, #8b5cf6 100%)'
            }}
          >
            <span className="text-white font-bold text-lg">B</span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-200">Banking as a Service</h1>
            <p className="text-xs text-slate-500">Animação Pedagógica • BCB CP 108/2024</p>
          </div>
        </div>

        {/* Navegação por seções */}
        <nav className="flex items-center gap-1">
          {sections.map((section) => (
            <button
              key={section.id}
              onClick={() => setCurrentSection(section.id)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 flex items-center gap-2 ${
                currentSection === section.id 
                  ? 'text-white' 
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
              style={currentSection === section.id ? {
                background: 'linear-gradient(135deg, rgba(14, 165, 233, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%)',
                border: '1px solid rgba(14, 165, 233, 0.3)'
              } : {}}
            >
              <span>{section.icon}</span>
              <span className="hidden lg:inline">{section.title}</span>
            </button>
          ))}
        </nav>

        {/* Controles */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="w-10 h-10 rounded-xl flex items-center justify-center transition-all hover:scale-105"
            style={{
              background: isPlaying ? 'rgba(16, 185, 129, 0.2)' : 'rgba(100, 116, 139, 0.2)',
              border: `1px solid ${isPlaying ? 'rgba(16, 185, 129, 0.5)' : 'rgba(100, 116, 139, 0.3)'}`
            }}
          >
            <span className={isPlaying ? 'text-emerald-400' : 'text-slate-400'}>
              {isPlaying ? '⏸' : '▶'}
            </span>
          </button>
        </div>
      </header>

      {/* Conteúdo principal */}
      <main className="flex-1 overflow-hidden">
        {renderSection()}
      </main>

      {/* Footer com navegação de seções */}
      <footer 
        className="flex items-center justify-between px-6 py-3 border-t"
        style={{ 
          background: 'rgba(15, 23, 42, 0.9)',
          borderColor: 'rgba(100, 116, 139, 0.2)'
        }}
      >
        <button
          onClick={() => setCurrentSection(Math.max(0, currentSection - 1))}
          disabled={currentSection === 0}
          className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all disabled:opacity-30 disabled:cursor-not-allowed hover:bg-slate-800/50"
          style={{ color: currentSection === 0 ? '#475569' : '#94a3b8' }}
        >
          ← Anterior
        </button>

        {/* Indicadores de progresso */}
        <div className="flex items-center gap-2">
          {sections.map((s) => (
            <div
              key={s.id}
              className={`w-2 h-2 rounded-full transition-all cursor-pointer hover:scale-150 ${
                currentSection === s.id ? 'w-6' : ''
              }`}
              style={{
                background: currentSection === s.id 
                  ? 'linear-gradient(90deg, #0ea5e9, #8b5cf6)' 
                  : 'rgba(100, 116, 139, 0.5)'
              }}
              onClick={() => setCurrentSection(s.id)}
            />
          ))}
        </div>

        <button
          onClick={() => setCurrentSection(Math.min(sections.length - 1, currentSection + 1))}
          disabled={currentSection === sections.length - 1}
          className="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all disabled:opacity-30 disabled:cursor-not-allowed hover:bg-slate-800/50"
          style={{ color: currentSection === sections.length - 1 ? '#475569' : '#94a3b8' }}
        >
          Próximo →
        </button>
      </footer>

      {/* Global Styles */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out forwards;
        }
        
        .hover\\:scale-102:hover {
          transform: scale(1.02);
        }
        
        ::-webkit-scrollbar {
          width: 8px;
        }
        
        ::-webkit-scrollbar-track {
          background: rgba(15, 23, 42, 0.5);
        }
        
        ::-webkit-scrollbar-thumb {
          background: rgba(100, 116, 139, 0.5);
          border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
          background: rgba(100, 116, 139, 0.7);
        }
      `}</style>
    </div>
  );
};

export default BaaSAnimation;
