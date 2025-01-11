import { mount } from '@vue/test-utils'
import { createStore } from 'vuex'
import Interfaces from '@/views/Interfaces.vue'

describe('Interfaces.vue', () => {
  let store
  let wrapper

  beforeEach(() => {
    store = createStore({
      state: {
        currentWebInterface: 'fluidd',
        interfaces: [
          { name: 'fluidd', status: 'active' },
          { name: 'mainsail', status: 'installed' }
        ]
      },
      actions: {
        switchInterface: jest.fn(),
        fetchInterfaces: jest.fn()
      }
    })

    wrapper = mount(Interfaces, {
      global: {
        plugins: [store]
      }
    })
  })

  it('renders interface buttons', () => {
    const buttons = wrapper.findAll('button')
    expect(buttons).toHaveLength(2)
    expect(buttons[0].text()).toContain('Fluidd')
    expect(buttons[1].text()).toContain('Mainsail')
  })

  it('highlights active interface', () => {
    const activeButton = wrapper.find('.active')
    expect(activeButton.text()).toContain('Fluidd')
  })

  it('disables button during switching', async () => {
    const button = wrapper.find('button')
    await button.trigger('click')
    expect(button.attributes('disabled')).toBeDefined()
  })

  it('shows loading state during switch', async () => {
    wrapper.vm.switching = true
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.loading-indicator').exists()).toBe(true)
  })

  it('handles switch interface action', async () => {
    const button = wrapper.find('button:last-child')
    await button.trigger('click')
    expect(store.actions.switchInterface).toHaveBeenCalledWith(
      expect.any(Object),
      'mainsail'
    )
  })

  it('shows error message on switch failure', async () => {
    store.actions.switchInterface.mockRejectedValue(new Error('Switch failed'))
    const button = wrapper.find('button:last-child')
    await button.trigger('click')
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.error-message').exists()).toBe(true)
  })

  it('fetches interfaces on mount', () => {
    expect(store.actions.fetchInterfaces).toHaveBeenCalled()
  })

  it('updates interface status after successful switch', async () => {
    store.actions.switchInterface.mockResolvedValue()
    const button = wrapper.find('button:last-child')
    await button.trigger('click')
    await wrapper.vm.$nextTick()
    expect(store.actions.fetchInterfaces).toHaveBeenCalled()
  })
})
